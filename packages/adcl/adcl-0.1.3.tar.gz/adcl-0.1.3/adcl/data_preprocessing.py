import os
import random
import string
import warnings

import numpy as np
import pandas as pd
import tensorflow as tf
from mxnet import gpu
import openml
from scipy.interpolate import UnivariateSpline
from dtaidistance import dtw
import matrixprofile as mp
from datetime import datetime

import datawig
import pyod
from pyod.models.knn import KNN
from pyod.models.ecod import ECOD
from pyod.utils.data import evaluate_print

from adtk.data import validate_series
from adtk.detector import LevelShiftAD, PersistAD
from adtk.transformer import DoubleRollingAggregate
from adtk.aggregator import AndAggregator

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, MinMaxScaler, StandardScaler, OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, KNNImputer
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Masking, InputLayer, Normalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

from category_encoders import CatBoostEncoder, TargetEncoder
warnings.filterwarnings('ignore')

#first preparation of dataframes/files, formats, separator, file type, NA values symbols, etc.
def ask_user_decision_df():
    """
    Asks the user to confirm whether the displayed DataFrame looks correct based on the head and info displayed.
    
    Returns:
        bool: True if the user confirms the DataFrame looks correct, False otherwise.
    """
    decision = input("Does the DataFrame look correct based on the head and info displayed? (yes/no): ").strip().lower()
    return decision.startswith('y')

def read_file_to_dataframe(train_filepath, test_filepath=None, separator=',', na_values='?', file_type=None):
    """
    Reads data from files into DataFrames, supporting CSV, Excel, and JSON formats.
    
    Args:
        train_filepath (str): The file path of the training data file.
        test_filepath (str, optional): The file path of the testing data file. Default is None.
        separator (str, optional): The delimiter used in CSV files. Default is ','.
        na_values (str, optional): Additional strings to recognize as NA/NaN. Default is '?'.
        file_type (str, optional): The type of file to read ('csv', 'xlsx', 'xls', 'json'). 
                                   If not provided, it's inferred from the file extension. Default is None.
        
    Returns:
        pd.DataFrame: The training DataFrame.
        pd.DataFrame: The testing DataFrame if 'test_filepath' is provided, otherwise None.
        
    Raises:
        ValueError: If the specified file is not found or the file type is unsupported.
    """
    def load_dataframe(filepath, file_type):
        if not os.path.exists(filepath):
            raise ValueError(f"File not found: {filepath}")
        if file_type == 'csv':
            df = pd.read_csv(filepath, sep=separator, na_values=na_values)
        elif file_type in ['xlsx', 'xls']:
            df = pd.read_excel(filepath, na_values=na_values)
        elif file_type == 'json':
            df = pd.read_json(filepath, orient='records')
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        print("DataFrame head:")
        print(df.head())
        print("\nDataFrame info:")
        df.info()

        return df if ask_user_decision_df() else None

    file_type = file_type or os.path.splitext(train_filepath)[-1][1:]
    df_train = load_dataframe(train_filepath, file_type)
    df_test = load_dataframe(test_filepath, file_type) if test_filepath else None
    return df_train, df_test

def check_dataframe_columns(df1, df2):
    """
    Checks if two pandas DataFrames have the same column names and order.
    
    Args:
        df1 (pd.DataFrame): The first DataFrame (e.g., X_train).
        df2 (pd.DataFrame): The second DataFrame (e.g., X_test).
    
    Returns:
        bool: True if both DataFrames have the same column names in the same order, False otherwise.
    """
    if list(df1.columns) == list(df2.columns):
        return True
    else:
        missing_in_df1 = set(df2.columns) - set(df1.columns)
        missing_in_df2 = set(df1.columns) - set(df2.columns)
        if missing_in_df1:
            print(f"Columns missing in the first DataFrame (e.g., X_train): {missing_in_df1}")
        if missing_in_df2:
            print(f"Columns missing in the second DataFrame (e.g., X_test): {missing_in_df2}")
        return False

def train_test_split_time_series(df, split_ratio=0.8, datetime_col='date'):
    """
    Splits a time series DataFrame into training and testing sets while maintaining chronological order
    and handling NaT values in the datetime column.
    
    Args:
        df (pd.DataFrame): The time series DataFrame to split. Should be sorted by datetime.
        split_ratio (float): The proportion of the dataset to include in the train split.
        datetime_col (str): The name of the column containing datetime information.
        
    Returns:
        pd.DataFrame: Training data (X_train).
        pd.DataFrame: Test data (X_test).
    """
    df_cleaned = df.dropna(subset=[datetime_col])
    df_sorted = df_cleaned.sort_values(by=datetime_col)
    split_idx = int(len(df_sorted) * split_ratio)
    X_train = df_sorted.iloc[:split_idx]
    X_test = df_sorted.iloc[split_idx:]
    return X_train, X_test

def preprocess_datetime_features(df1):
    """
    Preprocesses datetime features in a DataFrame by converting them to numerical representations
    using sine and cosine transformations for cyclic properties (e.g., day of year, month).
    
    Args:
        df1 (pd.DataFrame): The DataFrame containing datetime features to preprocess.
        
    Returns:
        pd.DataFrame: A copy of the input DataFrame with datetime features preprocessed.
                      Original datetime columns are dropped, and transformed features are added.
                      
    Note:
        This function assumes that the input DataFrame contains datetime columns.
    """
    df = df1.copy()
    datetime_cols = df.select_dtypes(include=['datetime', 'datetime64']).columns
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col])
        df[col + '_day_sin'] = np.sin(df[col].dt.dayofyear / 365 * 2 * np.pi)
        df[col + '_day_cos'] = np.cos(df[col].dt.dayofyear / 365 * 2 * np.pi)
        df[col + '_month_sin'] = np.sin((df[col].dt.month - 1) / 12 * 2 * np.pi)
        df[col + '_month_cos'] = np.cos((df[col].dt.month - 1) / 12 * 2 * np.pi)
        df[col + '_year'] = df[col].dt.year
        df.drop(columns=[col], inplace=True)
    return df

def prepare_datasets(df, df_test=None, target_var=None, data_type='cross', datetime_col=None):
    """
    Prepares training and testing datasets for machine learning tasks, including handling missing columns,
    splitting time series or cross-sectional data, and preprocessing datetime features if present.
    
    Args:
        df (pd.DataFrame): The main DataFrame containing the training data.
        df_test (pd.DataFrame, optional): The optional DataFrame containing the testing data. Default is None.
        target_var (str, optional): The name of the target variable column. Default is None.
        data_type (str): The type of data ('cross' for cross-sectional, 'time' for time series). Default is 'cross'.
        datetime_col (str, optional): The name of the column containing datetime information. Default is None.
        
    Returns:
        pd.DataFrame: Training data (X_train).
        pd.DataFrame: Test data (X_test).
        str: Name of the target variable column.
        str: Name of the datetime column.
        
    Notes:
        - If 'target_var' is provided but not found in 'df' columns, it prompts the user to enter the correct column name.
        - If 'data_type' is 'time' and 'datetime_col' is not provided, it prompts the user to enter the datetime column name.
        - If 'df_test' is not provided, it splits the 'df' into training and testing sets based on 'data_type'.
        - Preprocesses datetime features if present, including handling missing datetime columns and performing transformations.
    """
    if target_var and target_var not in df.columns:
        while True:
            response = input(f"There is no such column '{target_var}', write the correct column or leave empty to skip: ").strip()
            if response == '':
                target_var = None
                break
            elif response in df.columns:
                target_var = response
                break
    if data_type == 'time' and datetime_col == None:
        datetime_col = input("Please enter the name of the datetime column (default 'Date'): ").strip() or 'Date'
        if datetime_col not in df.columns:
            while True:
                datetime_col = input(f"There is no such column '{datetime_col}', write the correct column or leave empty to skip: ").strip()
                if datetime_col == '':
                    datetime_col = 'Date'
                    break
                if datetime_col in df.columns:
                    break
    if df_test is None:
        if data_type == 'cross':
            test_size = float(input("Enter the test size as a fraction (default 0.2): ").strip() or 0.2)
            random_state = int(input("Enter a random seed for reproducibility (default 42): ").strip() or 42)
            X_train, X_test = train_test_split(df, test_size=test_size, random_state=random_state)
        elif data_type == 'time':
            split_ratio = float(input("Enter the split ratio for time series (default 0.8): ").strip() or 0.8)
            X_train, X_test = train_test_split_time_series(df, split_ratio=split_ratio, datetime_col=datetime_col)
    else:
        X_train = df
        X_test = df_test

    y_column_name = target_var if target_var else np.nan
    date_col = datetime_col if datetime_col else np.nan
    datetime_cols = X_train.select_dtypes(include=['datetime', 'datetime64']).columns
    if len(datetime_cols)>0:
        if date_col is not np.NAN:
            date_col_train = X_train[date_col]
            date_col_test = X_test[date_col]
            X_train = X_train.drop(columns=[date_col])
            X_train = preprocess_datetime_features(X_train)
            X_test = X_test.drop(columns=[date_col])
            X_test = preprocess_datetime_features(X_test)
            X_train[date_col] = date_col_train
            X_test[date_col] = date_col_test
        else:
            X_train = preprocess_datetime_features(X_train)
            X_test = preprocess_datetime_features(X_test)
    return X_train, X_test, y_column_name, date_col

def ask_user_decision_conv(column_name, target_type):
    """
    Asks the user whether to discard non-conforming observations and convert a column to the specified target type.
    
    Args:
        column_name (str): The name of the column to convert.
        target_type (str): The target data type to convert the column to.
        
    Returns:
        bool: True if the user chooses to discard non-conforming observations and convert, False otherwise.
    """
    response = input(f"Column '{column_name}' has between 95% and 100% non-empty values that can be converted to {target_type}. "
                     "Would you like to discard non-conforming observations and convert? (yes/no): ")
    return response.lower().startswith('y')

def check_conversion_series(series, target_type):
    """
    Checks if a series can be successfully converted to the target data type and calculates the conversion success ratio.
    
    Args:
        series (pd.Series): The series to be converted.
        target_type (str): The target data type to convert the series to ('float', 'int', 'datetime').
        
    Returns:
        pd.Series: The converted series.
        float: The conversion success ratio, defined as the proportion of non-NA values successfully converted.
    """
    if target_type == 'float':
        converted_series = pd.to_numeric(series, errors='coerce')
    elif target_type == 'int':
        converted_series = pd.to_numeric(series, downcast='integer', errors='coerce')
    elif target_type == 'datetime':
        converted_series = pd.to_datetime(series, errors='coerce')
    else:
        raise ValueError(f"Unsupported target_type: {target_type}")
    non_na_original = series.dropna()
    conversion_success_ratio = converted_series.notna().sum() / non_na_original.size
    return converted_series, conversion_success_ratio

def infer_and_convert_dtypes(dataframe):
    """
    Automatically infers and converts the data types of columns in a DataFrame based on conversion success ratios.
    
    Args:
        dataframe (pd.DataFrame): The DataFrame to infer and convert data types.
        
    Returns:
        pd.DataFrame: The DataFrame with inferred and converted data types.
    """
    for column in dataframe.columns:
        original_series = dataframe[column]
        if original_series.dropna().empty:
            continue
        for target_type in ['float', 'int', 'datetime']:
            converted_series, conversion_success_ratio = check_conversion_series(original_series, target_type)
            if conversion_success_ratio == 1.0:
                dataframe[column] = converted_series
                print(f"Column '{column}' automatically converted to {target_type}.")
                break
            elif 0.95 <= conversion_success_ratio < 1.0:
                if ask_user_decision_conv(column, target_type):
                    dataframe[column] = converted_series.dropna()
                    print(f"Column '{column}' converted to {target_type} after discarding non-conforming observations.")
                else:
                    print(f"Column '{column}' retains original type upon user request.")
                break
    return dataframe

def process_data(train_input, test_input=None, separator=',', na_values='?', target_var=None, data_type='cross', file_type=None, datetime_col=None):
    """
    Processes the input data for machine learning tasks, including reading from files, handling different input types,
    checking column consistency between training and testing data, inferring and converting data types,
    and preparing datasets for training and testing.
    
    Args:
        train_input (str or pd.DataFrame): The file path or DataFrame containing the training data.
        test_input (str or pd.DataFrame, optional): The file path or DataFrame containing the testing data. Default is None.
        separator (str, optional): The delimiter used in CSV files. Default is ','.
        na_values (str, optional): Additional strings to recognize as NA/NaN. Default is '?'.
        target_var (str, optional): The name of the target variable column. Default is None.
        data_type (str): The type of data ('cross' for cross-sectional, 'time' for time series). Default is 'cross'.
        file_type (str, optional): The type of file to read ('csv', 'xlsx', 'xls', 'json'). 
                                   If not provided, it's inferred from the file extension. Default is None.
        datetime_col (str, optional): The name of the column containing datetime information. Default is None.
        
    Returns:
        pd.DataFrame: Training data (X_train).
        pd.DataFrame: Test data (X_test).
        str: Name of the target variable column.
        str: Name of the datetime column.
        
    Raises:
        ValueError: If the input type for training data is invalid or if column mismatch is detected between training and testing data.
        
    Notes:
        - If 'train_input' is a string, it's treated as a file path and read into a DataFrame.
        - If 'test_input' is provided, column consistency is checked between training and testing data.
        - Data types are inferred and converted for both training and testing DataFrames.
        - Datasets are prepared for training and testing, including handling datetime columns.
    """
    if isinstance(train_input, str):
        df_train, df_test = read_file_to_dataframe(train_input, test_input, separator, na_values, file_type)
    elif isinstance(train_input, pd.DataFrame):
        df_train = train_input
        df_test = test_input if isinstance(test_input, pd.DataFrame) else np.nan
    else:
        raise ValueError("Invalid input type for training data.")

    if isinstance(df_test, pd.DataFrame):
        if not check_dataframe_columns(df_train, df_test):
            print("Process terminated due to column mismatch.")
            return None, None, None
    df_train_conv = infer_and_convert_dtypes(df_train)
    try: 
        df_test_conv = infer_and_convert_dtypes(df_test) 
    except:
        df_test_conv = pd.DataFrame()
    X_train, X_test, y_column_name, datetime_col_final = prepare_datasets(df_train, df_test, target_var, data_type, datetime_col)
    return X_train, X_test, y_column_name, datetime_col_final

#encoding handeling
def one_hot_encoding(X_train1, X_test1):
    """
    Prepares the training and test datasets by applying one-hot encoding to categorical variables,
    assuming no missing values are present.
    
    Parameters:
    - X_train: pd.DataFrame, The training dataset.
    - X_test: pd.DataFrame, The test dataset.
    
    Returns:
    - X_train_encoded: pd.DataFrame, The training dataset with categorical variables one-hot encoded.
    - X_test_encoded: pd.DataFrame, The test dataset with categorical variables one-hot encoded.
    """
    X_train,X_test = X_train1.copy(),X_test1.copy()
    categorical_cols = X_train.select_dtypes(include=['object', 'category']).columns.tolist()
    encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
    preprocessor = ColumnTransformer(transformers=[('cat', encoder, categorical_cols)],remainder='passthrough')
    preprocessor.fit(X_train)
    X_train_encoded = preprocessor.transform(X_train)
    X_test_encoded = preprocessor.transform(X_test)
    try:
        encoded_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_cols)
        feature_names = list(encoded_feature_names) + [col for col in X_train.columns if col not in categorical_cols]
        X_train_encoded_df = pd.DataFrame(X_train_encoded, columns=feature_names, index=X_train.index)
        X_test_encoded_df = pd.DataFrame(X_test_encoded, columns=feature_names, index=X_test.index)
        return X_train_encoded_df, X_test_encoded_df
    except:
        return X_train, X_test

def label_encoding(X_train1, X_test1):
    """
    Performs label encoding on categorical columns in training and testing datasets.
    
    Args:
        X_train1 (pd.DataFrame): The training dataset.
        X_test1 (pd.DataFrame): The testing dataset.
        
    Returns:
        pd.DataFrame: Encoded training dataset (X_train_encoded).
        pd.DataFrame: Encoded testing dataset (X_test_encoded).
        
    Notes:
        - This function handles missing values in categorical columns by filling them with a unique placeholder.
        - Label encoding is performed using the LabelEncoder from scikit-learn.
        - Encoded placeholder values are replaced back with NaN in both datasets if 'NaN_placeholder' is a class.
    """
    X_train,X_test = X_train1.copy(),X_test1.copy()
    X_train_encoded,X_test_encoded = X_train.copy(),X_test.copy()
    categorical_cols = X_train.select_dtypes(include=['object', 'category']).columns.tolist()
    for col in categorical_cols:
        X_train_filled = X_train[col].fillna('NaN_placeholder')
        X_test_filled = X_test[col].fillna('NaN_placeholder')
        combined = pd.concat([X_train_filled, X_test_filled], ignore_index=True)
        le = LabelEncoder()
        le.fit(combined)
        X_train_encoded[col] = le.transform(X_train_filled)
        X_test_encoded[col] = le.transform(X_test_filled)
        if 'NaN_placeholder' in le.classes_:
            placeholder_index = list(le.classes_).index('NaN_placeholder')
            X_train_encoded[col] = X_train_encoded[col].replace(placeholder_index, np.NAN)
            X_test_encoded[col] = X_test_encoded[col].replace(placeholder_index, np.NAN)
    return X_train_encoded, X_test_encoded

def target_encoding(X_train1, X_test1, target_column_name):
    """
    Applies target encoding to each categorical column separately in the training and test datasets.
    
    Args:
        X_train1 (pd.DataFrame): The training dataset with input features and the target column.
        X_test1 (pd.DataFrame): The testing dataset with input features.
        target_column_name (str): The name of the target column in the training dataset.
        
    Returns:
        tuple: A tuple containing the transformed training and testing datasets.
    """
    X_train, X_test = X_train1.copy(), X_test1.copy()
    if target_column_name not in X_train.columns:
        raise ValueError(f"Target column '{target_column_name}' not found in training data.")
    y_train = X_train[target_column_name]
    X_train = X_train.drop(columns=[target_column_name])
    X_test = X_test.drop(columns=[target_column_name])
    categorical_cols = X_train.select_dtypes(include=['object', 'category']).columns.tolist()
    missing_in_X_test = set(X_train.columns) - set(X_test.columns)
    for col in missing_in_X_test:
        X_test[col] = np.nan
    X_test = X_test[X_train.columns]
    for col in categorical_cols:
        encoder = TargetEncoder()
        X_train[col] = encoder.fit_transform(X_train[col], y_train)
        X_test[col] = encoder.transform(X_test[col])
    return X_train, X_test

def catboost_encode(X_train1, X_test1, target_column_name):
    """
    Applies CatBoost encoding to the specified categorical columns in the training and test datasets.

    Parameters:
    - X_train: pd.DataFrame, training dataset.
    - y_train: pd.Series, target variable associated with X_train.
    - X_test: pd.DataFrame, test dataset.
    - cat_features: list of str, names of the categorical columns to be encoded.
    
    Returns:
    - X_train_encoded: pd.DataFrame, CatBoost encoded training dataset.
    - X_test_encoded: pd.DataFrame, CatBoost encoded test dataset.
    """
    X_train, X_test = X_train1.copy(), X_test1.copy()
    y_train = X_train[target_column_name]
    X_train = X_train.drop(columns=[target_column_name])
    X_test = X_test.drop(columns=[target_column_name])
    cat_features = X_train.select_dtypes(include=['object', 'category']).columns.tolist()
    encoder = CatBoostEncoder(cols=cat_features, handle_missing='value', handle_unknown='value')
    X_train_encoded = encoder.fit_transform(X_train, y_train)
    X_test_encoded = encoder.transform(X_test)
    return X_train_encoded, X_test_encoded

def encode_data(df_train, df_test, y_column_name=None,
                encoding_method='auto', nu=0.05, kernel='rbf', gamma='scale',
                n_neighbors=20, contamination='auto', n_estimators=100,
                encoding_dim=8, epochs=50, batch_size=32):
    """
    Encodes categorical features in training and testing datasets using various encoding methods.

    Args:
        df_train (pd.DataFrame): The training dataset.
        df_test (pd.DataFrame): The testing dataset.
        y_column_name (str, optional): The name of the target column for target encoding methods. Default is None.
        encoding_method (str): The encoding method to use. Options: 'auto', 'one_hot', 'label', 'target', 'catboost'. Default is 'auto'.
        nu (float): Anomaly detection parameter for outlier detection in CatBoost encoding. Default is 0.05.
        kernel (str): Kernel function for SVDD anomaly detection in CatBoost encoding. Default is 'rbf'.
        gamma (str): Kernel coefficient for 'rbf' kernel in CatBoost encoding. Default is 'scale'.
        n_neighbors (int): Number of neighbors for local outlier factor in CatBoost encoding. Default is 20.
        contamination (float): Proportion of outliers expected in the data for CatBoost encoding. Default is 'auto'.
        n_estimators (int): Number of trees for CatBoost encoding. Default is 100.
        encoding_dim (int): Dimensionality of the encoded representation for autoencoder-based methods. Default is 8.
        epochs (int): Number of epochs for training the autoencoder. Default is 50.
        batch_size (int): Batch size for training the autoencoder. Default is 32.

    Returns:
        pd.DataFrame: Encoded training dataset.
        pd.DataFrame: Encoded testing dataset.

    Raises:
        ValueError: If an invalid encoding method is specified or if required parameters are not provided.

    Notes:
        - If 'encoding_method' is set to 'auto', the method is automatically determined based on data characteristics.
        - CatBoost encoding and target encoding require the target column name ('y_column_name').
        - Autoencoder-based encoding methods require specifying 'encoding_dim', 'epochs', and 'batch_size'.
        - The user is prompted to choose between CatBoost and target encoding if the target column is specified and 'encoding_method' is set to 'auto'.
        - Label encoding is used if missing values are present in the data.
        - One-hot encoding is used by default if there are no missing values and no target column specified.
    """
    def apply_encoding(method):
        if method == 'one_hot':
            return one_hot_encoding(df_train, df_test)
        elif method == 'label':
            return label_encoding(df_train, df_test)
        elif method == 'target':
            if y_column_name:
                return target_encoding(df_train, df_test, y_column_name)
            else:
                raise ValueError("Target column name must be provided for target encoding.")
        elif method == 'catboost':
            if y_column_name:
                return catboost_encode(df_train, df_test, y_column_name)
            else:
                raise ValueError("Target column name must be provided for CatBoost encoding.")
    if encoding_method == 'auto':
        if y_column_name is not None and y_column_name in df_train.columns:
            choice = input("Do you prefer catboost encoding or target encoding? (Enter '1' for catboost or '2' for target): ")
            chosen_method = 'catboost' if choice == '1' else 'target'
        elif df_train.isnull().any().any() or df_test.isnull().any().any():
            chosen_method = 'label'
        else:
            chosen_method = 'one_hot'
    else:
        chosen_method = encoding_method
    return apply_encoding(chosen_method)

#missing values handeling
def impute_and_encode_MICE(X_train, X_test):
    """
    First, apply label encoding to categorical variables in X_train and X_test.
    Then, impute missing values using IterativeImputer (MICE).
    
    Parameters:
    - X_train: DataFrame, the training dataset.
    - X_test: DataFrame, the test dataset.
    
    Returns:
    - X_train_imputed_encoded: DataFrame, the training dataset with imputed and encoded values.
    - X_test_imputed_encoded: DataFrame, the test dataset with imputed and encoded values.
    """
    X_train_encoded, X_test_encoded = label_encoding(X_train, X_test)
    imputer = IterativeImputer(random_state=100, max_iter=10)
    imputer.fit(X_train_encoded)
    df_imputed_train = imputer.transform(X_train_encoded)
    df_imputed_test = imputer.transform(X_test_encoded)
    X_train_encoded.loc[:, :] = df_imputed_train
    X_test_encoded.loc[:, :] = df_imputed_test
    X_train_imputed_encoded = pd.DataFrame(df_imputed_train, index=X_train.index, columns=X_train_encoded.columns)
    X_test_imputed_encoded = pd.DataFrame(df_imputed_test, index=X_test.index, columns=X_test_encoded.columns)
    return X_train_imputed_encoded, X_test_imputed_encoded

def impute_and_encode_KNN(X_train, X_test):
    """
    First, apply label encoding to categorical variables in X_train and X_test.
    Then, impute missing values using KNNImputer.
    
    Parameters:
    - X_train: DataFrame, the training dataset.
    - X_test: DataFrame, the test dataset.
    
    Returns:
    - X_train_imputed_encoded: DataFrame, the training dataset with imputed and encoded values.
    - X_test_imputed_encoded: DataFrame, the test dataset with imputed and encoded values.
    """
    X_train_encoded, X_test_encoded = label_encoding(X_train, X_test)
    imputer = KNNImputer(n_neighbors=5, weights="uniform")
    imputer.fit(X_train_encoded)
    df_imputed_train = imputer.transform(X_train_encoded)
    df_imputed_test = imputer.transform(X_test_encoded)
    X_train_encoded.loc[:, :] = df_imputed_train
    X_test_encoded.loc[:, :] = df_imputed_test
    X_train_imputed_encoded = pd.DataFrame(df_imputed_train, index=X_train.index, columns=X_train_encoded.columns)
    X_test_imputed_encoded = pd.DataFrame(df_imputed_test, index=X_test.index, columns=X_test_encoded.columns)
    return X_train_imputed_encoded, X_test_imputed_encoded

def impute_datawig(X_train, X_test):
    X_train_encoded, X_test_encoded = label_encoding(X_train, X_test)
    columns_with_missing_values = X_train.columns[X_train.isna().any()].tolist()
    for col in columns_with_missing_values:
        imputer = datawig.SimpleImputer(
            input_columns=[c for c in X_train.columns if c != col and X_train[c].dtype != 'object'],output_column=col)
        imputer.fit(X_train_encoded, num_epochs=50)
        X_train_imputed = imputer.predict(X_train_encoded)
        X_test_imputed = imputer.predict(X_test_encoded)
        if col + '_imputed' in X_train_imputed.columns:
            X_train_encoded[col].fillna(X_train_imputed[col + '_imputed'], inplace=True)
            X_test_encoded[col].fillna(X_test_imputed[col + '_imputed'], inplace=True)
        if col + '_imputed' in X_train_encoded.columns:
            X_train_encoded.drop(columns=[col + '_imputed'], inplace=True)
        if col + '_imputed' in X_test_encoded.columns:
            X_test_encoded.drop(columns=[col + '_imputed'], inplace=True)
    return X_train_encoded, X_test_encoded

def interpolate_and_fill(train_df, test_df, time_col):
    train_df_temp = train_df.copy()
    test_df_temp = test_df.copy()
    train_df_temp[time_col] = pd.to_datetime(train_df_temp[time_col], errors='coerce')
    test_df_temp[time_col] = pd.to_datetime(test_df_temp[time_col], errors='coerce')
    train_df_temp[time_col].fillna(method='ffill', inplace=True)
    train_df_temp[time_col].fillna(method='bfill', inplace=True)
    test_df_temp[time_col].fillna(method='ffill', inplace=True)
    test_df_temp[time_col].fillna(method='bfill', inplace=True)
    if train_df_temp[time_col].isnull().any() or test_df_temp[time_col].isnull().any():
        raise ValueError("NaN values cannot be filled in the time column. Please check your data!")
    train_df_temp.set_index(time_col, inplace=True)
    test_df_temp.set_index(time_col, inplace=True)
    train_interpolated = train_df_temp.interpolate(method='time')
    test_interpolated = test_df_temp.interpolate(method='time')
    train_interpolated.fillna(method='ffill', inplace=True)
    train_interpolated.fillna(method='bfill', inplace=True)
    test_interpolated.fillna(method='ffill', inplace=True)
    test_interpolated.fillna(method='bfill', inplace=True)
    train_interpolated.reset_index(inplace=True)
    test_interpolated.reset_index(inplace=True)
    return train_interpolated, test_interpolated

def spline_interpolate_with_text_fill(df, datetime_col='Date', order=3):
    df = df.sort_values(by=datetime_col)
    df['Date_ordinal'] = pd.to_numeric(df[datetime_col].map(lambda x: x.toordinal() if pd.notnull(x) else np.nan), downcast='integer')
    for col in df.columns:
        if col not in [datetime_col, 'Date_ordinal'] and df[col].dtype in [np.float64, np.int64]:
            valid_idx = df[col].notna() & df['Date_ordinal'].notna()
            if valid_idx.sum() > order:
                spline = UnivariateSpline(df.loc[valid_idx, 'Date_ordinal'], df.loc[valid_idx, col], k=order)
                missing_idx = df[col].isna() & df['Date_ordinal'].notna()
                df.loc[missing_idx, col] = spline(df.loc[missing_idx, 'Date_ordinal'])
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna(method='ffill').fillna(method='bfill')
    df.drop(columns=['Date_ordinal'], inplace=True)
    return df

def linear_interpolate_with_text_fill(df, datetime_col='Date'):
    """
    Performs linear interpolation on numeric columns of a dataframe based on a specified datetime column,
    and fills missing values in non-numeric columns by forward fill and backward fill methods.
    
    Args:
    - df (pd.DataFrame): DataFrame to interpolate.
    - datetime_col (str): Name of the datetime column.
    
    Returns:
    - pd.DataFrame: DataFrame with interpolated values for numeric columns and filled values for non-numeric columns.
    """
    df = df.sort_values(by=datetime_col)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].interpolate(method='linear')
    non_numeric_cols = df.select_dtypes(exclude=[np.number, 'datetime64[ns]']).columns
    df[non_numeric_cols] = df[non_numeric_cols].fillna(method='ffill').fillna(method='bfill')
    return df

def enhanced_locf_imputation(X_train, X_test, datetime_col='Date'):
    """
    Enhanced LOCF imputation that also considers initial missing values by applying
    a backward fill as a secondary step.
    
    Args:
        X_train (pd.DataFrame): Training dataset.
        X_test (pd.DataFrame): Testing dataset.
        datetime_col (str): Column name for the datetime variable.
        
    Returns:
        pd.DataFrame: Enhanced LOCF imputed training dataset.
        pd.DataFrame: Enhanced LOCF imputed testing dataset.
    """
    X_train_sorted = X_train.sort_values(by=datetime_col)
    X_test_sorted = X_test.sort_values(by=datetime_col)
    X_train_imputed = X_train_sorted.fillna(method='ffill').fillna(method='bfill')
    X_test_imputed = X_test_sorted.fillna(method='ffill').fillna(method='bfill')
    return X_train_imputed, X_test_imputed

def create_sequences(X, n_steps):
    sequences = []
    for i in range(len(X) - n_steps + 1):
        sequence = X[i:(i + n_steps)]
        sequences.append(sequence)
    return np.array(sequences)

def rnn_impute(X_train, X_test, n_steps=10, unique_mask_value=-999):
    if X_train.select_dtypes(include=['object']).shape[1] > 0 or X_test.select_dtypes(include=['object']).shape[1] > 0:
        X_train, X_test = label_encoding(X_train, X_test)
    X_train_processed = preprocess_datetime_features(X_train.copy())
    X_test_processed = preprocess_datetime_features(X_test.copy())
    nan_locations_train = X_train_processed.isna()
    nan_locations_test = X_test_processed.isna()
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train_processed.fillna(0))
    X_test_scaled = scaler.transform(X_test_processed.fillna(0))
    X_train_seq = create_sequences(X_train_scaled, n_steps)
    X_test_seq = create_sequences(X_test_scaled, n_steps)
    X_train_seq_masked = np.nan_to_num(X_train_seq, nan=unique_mask_value)
    X_test_seq_masked = np.nan_to_num(X_test_seq, nan=unique_mask_value)
    model = Sequential([Masking(mask_value=unique_mask_value, input_shape=(X_train_seq.shape[1], X_train_seq.shape[2])),
        LSTM(100, return_sequences=True, activation='relu'),
        Dense(X_train_seq.shape[2])])
    model.compile(optimizer='adam', loss='mse')
    early_stopping = EarlyStopping(monitor='loss', patience=5, min_delta=0.0001)
    model.fit(X_train_seq_masked, X_train_seq_masked, epochs=50, verbose=1, callbacks=[early_stopping])
    X_train_imputed_seq = model.predict(X_train_seq_masked)
    X_test_imputed_seq = model.predict(X_test_seq_masked)
    X_train_imputed = X_train_imputed_seq[:, -1, :]
    X_train_imputed_full = scaler.inverse_transform(X_train_imputed)
    X_train_final = X_train_processed.where(~nan_locations_train, pd.DataFrame(X_train_imputed_full, columns=X_train_processed.columns))
    X_test_imputed = X_test_imputed_seq[:, -1, :]
    X_test_imputed_full = scaler.inverse_transform(X_test_imputed)
    X_test_final = X_test_processed.where(~nan_locations_test, pd.DataFrame(X_test_imputed_full, columns=X_test_processed.columns))
    X_train_last, X_test_last = interpolate_and_fill(X_train, X_test, 'Date')
    return X_train_last, X_test_last

def missing_values_handling(df_train, df_test, datetime_col=np.nan, imputation_method='auto', n_steps=10, unique_mask_value=-999, order=3):
    """
    Function to handle missing values for both time-series and cross-sectional data.
    Automatically chooses an imputation method based on data type and user input.

    Args:
        df_train (pd.DataFrame): Training dataset.
        df_test (pd.DataFrame): Test dataset.
        datetime_col (str or np.nan): Column name of the datetime variable, or np.nan for cross-sectional data.
        imputation_method (str): Specifies the method to use for imputation ('auto', 'mice', 'knn', 'datawig', 'linear', 'spline', 'locf', 'rnn', 'time').
        n_steps (int): Number of steps for RNN imputation.
        order (int): Order of the spline for spline interpolation.

    Returns:
        pd.DataFrame: Imputed training dataset.
        pd.DataFrame: Imputed test dataset.
    """
    X_train, X_test = df_train.copy(), df_test.copy()

    if datetime_col is not np.nan:
        if imputation_method == 'auto':
            imputation_method = 'time'
        if imputation_method == 'time':
            return interpolate_and_fill(X_train, X_test, datetime_col)
        elif imputation_method == 'linear':
            X_train = linear_interpolate_with_text_fill(X_train, datetime_col)
            X_test = linear_interpolate_with_text_fill(X_test, datetime_col)
        elif imputation_method == 'spline':
            X_train = spline_interpolate_with_text_fill(X_train, datetime_col, order)
            X_test = spline_interpolate_with_text_fill(X_test, datetime_col, order)
        elif imputation_method == 'locf':
            X_train = enhanced_locf_imputation(X_train, datetime_col)
            X_test = enhanced_locf_imputation(X_test, datetime_col)
        elif imputation_method == 'rnn':
            X_train, X_test = rnn_impute(X_train, X_test, n_steps, unique_mask_value)
        else:
            raise ValueError("Unsupported imputation method for time-series data.")
    else:
        if imputation_method == 'auto':
            imputation_method = 'datawig'
        if imputation_method == 'mice':
            X_train, X_test = impute_and_encode_MICE(X_train, X_test)
        elif imputation_method == 'knn':
            X_train, X_test = impute_and_encode_KNN(X_train, X_test)
        elif imputation_method == 'datawig':
            X_train, X_test = impute_datawig(X_train, X_test)
        elif imputation_method == 'rnn':
            X_train, X_test = rnn_impute(X_train, X_test, n_steps, unique_mask_value)
        else:
            raise ValueError("Unsupported imputation method for cross-sectional data.")
    return X_train, X_test

#outliers handeling
def detect_outliers_ocsvm(X_train, X_test, nu=0.05, kernel='rbf', gamma='scale'):
    """
    Detect outliers in training and testing dataframes using One-Class SVM, appending the results as a new column.
    
    Parameters:
    - X_train: DataFrame, training data for the One-Class SVM.
    - X_test: DataFrame, testing data to detect outliers.
    - nu: float, an upper bound on the fraction of training errors and a lower bound of the fraction of support vectors.
    - kernel: str, specifies the kernel type to be used in the algorithm.
    - gamma: str, kernel coefficient for 'rbf', 'poly', and 'sigmoid'.
    
    Returns:
    - X_train: DataFrame, original training data with an additional column 'outlier_label_OCSVM'.
    - X_test: DataFrame, original testing data with an additional column 'outlier_label_OCSVM'.
    """
    X_train,X_test = X_train.copy(), X_test.copy()
    oc_svm = OneClassSVM(nu=nu, kernel=kernel, gamma=gamma)
    oc_svm.fit(X_train)
    train_outliers = oc_svm.predict(X_train)
    test_outliers = oc_svm.predict(X_test)
    X_train['outlier_label_OCSVM'] = (train_outliers == -1).astype(int)
    X_test['outlier_label_OCSVM'] = (test_outliers == -1).astype(int)
    return X_train, X_test

def detect_outliers_lof(X_train, X_test, n_neighbors=20, contamination='auto'):
    """
    Detect outliers in training and testing dataframes using Local Outlier Factor (LOF),
    appending the results as a new column.
    
    Parameters:
    - X_train: DataFrame, training data for fitting the LOF model.
    - X_test: DataFrame, testing data to detect outliers.
    - n_neighbors: int, number of neighbors to use for kneighbors queries.
    - contamination: 'auto' or float, the proportion of outliers in the data set.
    
    Returns:
    - X_train: DataFrame, original training data with an additional column 'outlier_label_LOF'.
    - X_test: DataFrame, original testing data with an additional column 'outlier_label_LOF'.
    """
    X_train,X_test = X_train.copy(), X_test.copy()
    lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination, novelty=True)
    lof.fit(X_train)
    train_outliers = lof.predict(X_train)
    test_outliers = lof.predict(X_test)
    X_train['outlier_label_LOF'] = (train_outliers == -1).astype(int)
    X_test['outlier_label_LOF'] = (test_outliers == -1).astype(int)
    return X_train, X_test

def detect_outliers_iforest(X_train, X_test, n_estimators=100, contamination='auto'):
    """
    Detect outliers in training and testing dataframes using Isolation Forest,
    appending the results as a new column.
    
    Parameters:
    - X_train: DataFrame, training data for fitting the Isolation Forest model.
    - X_test: DataFrame, testing data to detect outliers.
    - n_estimators: int, the number of base estimators in the ensemble.
    - contamination: 'auto' or float, the proportion of outliers in the data set.
    
    Returns:
    - X_train: DataFrame, original training data with an additional column 'outlier_label_iFores'.
    - X_test: DataFrame, original testing data with an additional column 'outlier_label_iFores'.
    """
    iforest = IsolationForest(n_estimators=n_estimators, contamination=contamination)
    iforest.fit(X_train)
    train_outliers = iforest.predict(X_train)
    test_outliers = iforest.predict(X_test)
    X_train['outlier_label_iFores'] = (train_outliers == -1).astype(int)
    X_test['outlier_label_iFores'] = (test_outliers == -1).astype(int)
    return X_train, X_test

def detect_outliers_autoencoder(X_train, X_test, encoding_dim=8, epochs=50, batch_size=32):
    """
    Detect outliers in training and testing dataframes using an Autoencoder.
    Parameters:
    - X_train: DataFrame, training data for fitting the Autoencoder.
    - X_test: DataFrame, testing data to detect outliers.
    - encoding_dim: int, number of dimensions in the encoded representation.
    - epochs: int, number of epochs for training the Autoencoder.
    - batch_size: int, batch size for training.
    Returns:
    - X_train_out: DataFrame, original training data with an additional column 'outlier_label_AE'.
    - X_test_out: DataFrame, original testing data with an additional column 'outlier_label_AE'.
    """
    X_train,X_test = X_train.copy(), X_test.copy()
    normalizer = Normalization(axis=-1)
    normalizer.adapt(X_train)
    X_train_scaled = normalizer(X_train)
    X_test_scaled = normalizer(X_test)
    input_dim = X_train_scaled.shape[1]
    model = Sequential([
        InputLayer(input_shape=(input_dim,)),
        Dense(encoding_dim, activation='relu'),
        Dense(input_dim, activation='sigmoid')])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train_scaled, X_train_scaled, epochs=epochs, batch_size=batch_size, shuffle=True, verbose=0)
    X_train_pred = model.predict(X_train_scaled)
    train_mse = np.mean(np.power(X_train_scaled - X_train_pred, 2), axis=1)
    train_threshold = np.percentile(train_mse, 95)
    train_outliers = train_mse > train_threshold
    X_test_pred = model.predict(X_test_scaled)
    test_mse = np.mean(np.power(X_test_scaled - X_test_pred, 2), axis=1)
    test_outliers = test_mse > train_threshold
    X_train_out = X_train.assign(outlier_label_AE=train_outliers.astype(int))
    X_test_out = X_test.assign(outlier_label_AE=test_outliers.astype(int))
    return X_train_out, X_test_out

def detect_outliers_sublof(X_train, X_test, datetime_col, window_size=20):
    """
    Detect outliers in time series training and testing dataframes using a subsequence-based LOF approach.
    Parameters:
    - X_train: DataFrame, training time series data.
    - X_test: DataFrame, testing time series data.
    - datetime_col: str, the name of the column containing datetime information.
    - window_size: int, size of the window to consider for creating subsequences.
    
    Returns:
    - X_train_out: DataFrame, original training data with an additional column 'outlier_label_SubLOF'.
    - X_test_out: DataFrame, original testing data with an additional column 'outlier_label_SubLOF'.
    """
    X_train = X_train.copy()
    X_test = X_test.copy()
    X_train[datetime_col] = pd.to_datetime(X_train[datetime_col])
    X_test[datetime_col] = pd.to_datetime(X_test[datetime_col])
    X_train.sort_values(by=datetime_col, inplace=True)
    X_test.sort_values(by=datetime_col, inplace=True)
    time_series_train = X_train[datetime_col].values
    profile_train = mp.compute(time_series_train, windows=window_size)
    profile_train = mp.discover.discords(profile_train)
    train_outlier_indices = profile_train['discords']
    train_outlier_labels = np.zeros(len(time_series_train), dtype=int)
    train_outlier_labels[train_outlier_indices] = 1
    X_train['outlier_label_SubLOF'] = train_outlier_labels
    time_series_test = X_test[datetime_col].values
    profile_test = mp.compute(time_series_test, windows=window_size)
    profile_test = mp.discover.discords(profile_test)
    test_outlier_indices = profile_test['discords']
    test_outlier_labels = np.zeros(len(time_series_test), dtype=int)
    test_outlier_labels[test_outlier_indices] = 1
    X_test['outlier_label_SubLOF'] = test_outlier_labels
    return X_train, X_test

def detect_outliers_dtw(X_train, X_test, datetime_col):
    """
    Detect outliers in time series training and testing data using Dynamic Time Warping (DTW) method.
    Parameters:
    - X_train: DataFrame, training time series data.
    - X_test: DataFrame, testing time series data.
    - datetime_col: str, the name of the column containing datetime information.
    
    Returns:
    - X_train_out: DataFrame, original training data with an additional column 'outlier_label_DTW'.
    - X_test_out: DataFrame, original testing data with an additional column 'outlier_label_DTW'.
    """
    X_train,X_test = X_train.copy(), X_test.copy()
    X_train = X_train.sort_values(by=datetime_col)
    X_test = X_test.sort_values(by=datetime_col)
    scaler = StandardScaler()
    train_series = scaler.fit_transform(X_train.drop(columns=[datetime_col]).values)
    test_series = scaler.transform(X_test.drop(columns=[datetime_col]).values)
    ref_series = np.median(train_series, axis=0)
    train_dtw_distances = np.array([dtw.distance(ref_series, train) for train in train_series])
    test_dtw_distances = np.array([dtw.distance(ref_series, test) for test in test_series])
    threshold = np.percentile(train_dtw_distances, 95)
    train_outlier_labels = train_dtw_distances > threshold
    test_outlier_labels = test_dtw_distances > threshold
    X_train_out = X_train.copy()
    X_train_out['outlier_label_DTW'] = train_outlier_labels.astype(int)
    X_test_out = X_test.copy()
    X_test_out['outlier_label_DTW'] = test_outlier_labels.astype(int)
    return X_train_out, X_test_out

def detect_anomalies_adtk_multivariate(X_train, X_test, datetime_col, window_size=30):
    """
    Detect anomalies in multivariate time series training and testing datasets using ADTK.

    Parameters:
    - X_train: DataFrame, the training time series data.
    - X_test: DataFrame, the testing time series data.
    - datetime_col: String, the name of the column containing datetime information.
    - window_size: Integer, size of the rolling window for DoubleRollingAggregate.

    Returns:
    - X_train, X_test: DataFrames with an additional 'outlier_label_ADTK' column indicating anomalies.
    """
    def process_data(df):
        df[datetime_col] = pd.to_datetime(df[datetime_col])
        df.set_index(datetime_col, inplace=True)
        validated_series = {col: validate_series(df[col]) for col in df.columns if col != datetime_col}
        combined_anomalies = pd.Series(False, index=df.index)
        for col, series in validated_series.items():
            transformer = DoubleRollingAggregate(agg='mean', window=window_size, center=True)
            transformed_series = transformer.transform(series)
            level_shift_ad = LevelShiftAD(c=6.0, side='both', window=window_size)
            persist_ad = PersistAD(c=3.0, side='positive', window=window_size)
            anomalies_level_shift = level_shift_ad.fit_detect(transformed_series)
            anomalies_persist = persist_ad.fit_detect(transformed_series)
            combined_anomalies_col = AndAggregator().aggregate(pd.concat([anomalies_level_shift, anomalies_persist], axis=1))
            combined_anomalies = combined_anomalies | combined_anomalies_col
        return combined_anomalies.astype(int)
    X_trainn, X_testn = X_train.copy(), X_test.copy()
    X_trainn['outlier_label_ADTK'] = process_data(X_trainn)
    X_testn['outlier_label_ADTK'] = process_data(X_testn)
    return X_trainn, X_testn

def outlier_detection(X_train, X_test, datetime_col=np.nan, method='auto', nu=0.05, kernel='rbf', gamma='scale',
                      n_neighbors=20, contamination='auto', n_estimators=100, encoding_dim=8, epochs=50, batch_size=32,
                      window_size=20, dtw_window=None):
    """
    Function to detect outliers in both time-series and cross-sectional data.
    Automatically chooses an imputation method based on data type and user input.

    Args:
        X_train (pd.DataFrame): Training dataset.
        X_test (pd.DataFrame): Testing dataset.
        datetime_col (str or np.nan): Column name of the datetime variable, or np.nan for cross-sectional data.
        method (str): Method to use for detecting outliers ('auto', 'ocsvm', 'lof', 'iforest', 'autoencoder', 'sublof', 'dtw', 'adtk').
        nu, kernel, gamma (float, str, str): Parameters for One-Class SVM.
        n_neighbors, contamination (int, str): Parameters for Local Outlier Factor.
        n_estimators (int): Parameter for Isolation Forest.
        encoding_dim, epochs, batch_size (int, int, int): Parameters for Autoencoder.
        window_size (int): Window size for SubLOF and ADTK.
        dtw_window (int or None): Window size for DTW, if applicable.

    Returns:
        tuple: (X_train_out, X_test_out) DataFrames with additional columns indicating detected outliers.
    """
    if pd.isna(datetime_col):
        if method == 'auto':
            method = 'autoencoder'
        if method == 'ocsvm':
            return detect_outliers_ocsvm(X_train, X_test, nu=nu, kernel=kernel, gamma=gamma)
        elif method == 'lof':
            return detect_outliers_lof(X_train, X_test, n_neighbors=n_neighbors, contamination=contamination)
        elif method == 'iforest':
            return detect_outliers_iforest(X_train, X_test, n_estimators=n_estimators, contamination=contamination)
        elif method == 'autoencoder':
            return detect_outliers_autoencoder(X_train, X_test, encoding_dim=encoding_dim, epochs=epochs, batch_size=batch_size)
        else:
            raise ValueError("Unsupported or invalid method for cross-sectional outlier detection.")
    else:
        if method == 'auto':
            method = 'adtk'
        
        if method == 'sublof':
            return detect_outliers_sublof(X_train, X_test, datetime_col, window_size=window_size)
        elif method == 'dtw':
            return detect_outliers_dtw(X_train, X_test, datetime_col)
        elif method == 'adtk':
            return detect_anomalies_adtk_multivariate(X_train, X_test, datetime_col, window_size=window_size)
        else:
            raise ValueError("Unsupported or invalid method for time-series outlier detection.")
    return None, None

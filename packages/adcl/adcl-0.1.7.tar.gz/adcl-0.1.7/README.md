# ADCL-Automatic-Data-Cleaning Project

## Overview
ADCL-Automatic-Data-Cleaning is a Python package designed to facilitate automated data cleaning, particularly leveraging deep learning techniques for preprocessing tasks essential in data science and machine learning workflows.

## Features
- **Data Preprocessing**: Standardize, normalize, and format your data for machine learning models.
- **Missing Value Imputation**: Implements various techniques for handling missing data in both cross-sectional and time-series datasets.
- **Outlier Detection**: Identifies and manages outliers using multiple strategies, improving the robustness of your models.
- **Encoding and Transformation**: Converts categorical data into a machine-readable format using various encoding techniques.
- **Time Series Handling**: Special functions for processing time-dependent data.

## Repository Structure
- **data_preprocessing/**: Contains the core library file `data_preprocessing.py` with all preprocessing functions.
- **examples/**: Includes `example_usage.ipynb`, a Jupyter notebook demonstrating how to use the preprocessing functions.
- **missing_values_imputation_test/**: Contains notebooks for testing missing value imputation across different data types.
- **outlier_detection_test/**: Contains notebooks for testing outliers detection across different data types.
- **LICENSE**: The project is open-sourced under the MIT license.

## Installation
To install ADCL directly from PyPI, run the following command:
```bash
pip install adcl
```

## Usage
### Data Preprocessing
You can preprocess your datasets by importing functions from `data_preprocessing.py`. For example:
```python
from adcl import process_data
filepath = 'path_to_your_data.csv'
df_train, df_test, y_column_name, date_col = process_data(train_input=filepath)
```

### Missing Value Handling
Handle missing values by choosing an appropriate method from the library. An example usage for time series data:
```python
from adcl import missing_values_handling
X_train_mis, X_test_mis = missing_values_handling(df_train=X_train, df_test=X_test, datetime_col=date_col, imputation_method='auto')
```

### Outlier Detection
Detect Outliers by choosing an appropriate method from the library. An example usage for time series data:
```python
from adcl import outlier_detection
X_train_out, X_test_out = outlier_detection(X_train=X_train, X_test=X_test, datetime_col=date_col
                                    , method='auto', nu=0.05, kernel='rbf', gamma='scale'
                                    , n_neighbors=20, contamination='auto', n_estimators=100
                                    , encoding_dim=8, epochs=50, batch_size=32
                                    , window_size=20, dtw_window=None)
```

### Categorical Variables Encoding
Encode categorical variables by choosing an appropriate method from the library. An example usage for time series data:
```python
from adcl import encode_data
X_train_enc, X_test_enc = encode_data(df_train=X_train, df_test=X_test, y_column_name,
                encoding_method='label', nu=0.05, kernel='rbf', gamma='scale',
                n_neighbors=20, contamination='auto', n_estimators=100,
                encoding_dim=8, epochs=50, batch_size=32)
```

### Example Notebooks
For detailed examples, refer to the notebooks in the `examples/` directory. These notebooks provide comprehensive guides on utilizing the package's functionalities effectively.

## Contributing
Contributions are welcome! If you have suggestions for improving the library, feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any queries or further information, please contact [steve19992@mail.ru](mailto:steve19992@mail.ru).

By providing structured guidance on using the package and clearly explaining what each part of the package does, users of all levels can effectively integrate ADCL into their data cleaning and preprocessing workflows.

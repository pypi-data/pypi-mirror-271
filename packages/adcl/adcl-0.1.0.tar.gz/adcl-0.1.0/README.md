# README for ADCL-Automatic-Data-Cleaning Project

## Overview
ADCL-Automatic-Data-Cleaning is a Python package designed to facilitate automated data cleaning, particularly leveraging deep learning techniques. This project focuses on improving accuracy and efficiency in preprocessing tasks essential for data science and machine learning workflows.

## Features
- **Data Preprocessing:** Standardize, normalize, and format your data for machine learning models.
- **Missing Value Imputation:** Implements various techniques for handling missing data in both cross-sectional and time-series datasets.
- **Outlier Detection:** Identifies and manages outliers using multiple strategies, improving the robustness of your models.
- **Encoding and Transformation:** Converts categorical data into a machine-readable format using various encoding techniques.
- **Time Series Handling:** Special functions for processing time-dependent data.

## Repository Structure
- `data_preprocessing/`
  - **data_preprocessing.py**: Core library file containing all preprocessing functions, including data cleaning, encoding, and preparation.
- `examples/`
  - **example_usage.ipynb**: Jupyter notebook demonstrating how to use the preprocessing functions.
- `missing_values_imputation_test/`
  - **missing_values_cross_sectional.ipynb**: Notebook for testing missing value imputation in cross-sectional data.
  - **missing_values_time_series.ipynb**: Notebook for testing missing value imputation in time series data.
- `cross_miss_results/`: Folder containing the results from the cross-sectional missing value tests.
- `time_miss_results/`: Folder containing the results from the time series missing value tests.
- **LICENSE**: The project is open-sourced under the MIT license.

## Installation
To get started with ADCL, clone this repository and install the required packages:

```bash
git clone https://github.com/yourgithub/ADCL-Automatic-Data-Cleaning.git
cd ADCL-Automatic-Data-Cleaning
pip install -r requirements.txt
```

## Usage
### Data Preprocessing
You can preprocess your datasets by importing functions from `data_preprocessing.py`. For example:

```python
from data_preprocessing import process_data
filepath = 'shares_datasets/AAPL.csv'
df_train, df_test, y_column_name, date_col = process_data(train_input=filepath, test_input=None, separator=',', na_values='?', target_var=None, data_type='time', file_type=None, datetime_col='Date')
```

### Missing Value Handling
Handle missing values by choosing an appropriate method from the library. An example usage for time series data:

```python
from data_preprocessing import missing_values_handling
X_train_mis, X_test_mis = missing_values_handling(df_train=X_train_enc, df_test=X_test_enc
                                                  , datetime_col=date_col, imputation_method='auto'
                                                  , n_steps=10, order=3)
```

### Example Notebooks
For the detailed examples, refer to the notebooks in the `examples/` directory. These notebooks provide comprehensive guides on utilizing the package's functionalities effectively.

## Contributing
Contributions are welcome! If you have suggestions for improving the library, feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For any queries or further information, please contact steve19992@mail.ru.

By providing structured guidance on using the package and clearly explaining what each part of the package does, users of all levels can effectively integrate ADCL into their data cleaning and preprocessing workflows.

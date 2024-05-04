# Data Quality Checks

This repository contains a collection of functions implemented in PySpark for conducting data quality checks on a DataFrame. These functions are useful for ensuring the reliability and consistency of your data before performing further analysis or machine learning tasks.

## Functions Included

1. **check_missing_values(df)**
    - Checks for missing values in a DataFrame.
  
2. **check_data_types(df)**
    - Checks the data types of columns in a DataFrame.
  
3. **check_duplicates(df, subset=None)**
    - Checks for duplicate rows in a DataFrame.
  
4. **check_outliers(df, numerical_cols, threshold=3)**
    - Checks for potential outliers in numerical columns using Z-score method.
  
5. **check_unique_values(df, categorical_cols)**
    - Checks the uniqueness of values in categorical columns of a DataFrame.
  
6. **check_column_lengths(df, string_cols, max_length)**
    - Checks the lengths of string columns in a DataFrame.
  
7. **check_nullability(df, nullable_cols)**
    - Checks the nullability of columns in a DataFrame.
  
8. **check_data_range(df, numerical_cols, min_val=None, max_val=None)**
    - Checks the range of values in numerical columns of a DataFrame.
  
9. **check_nulls_in_specific_cols(df, specific_cols)**
    - Checks for missing values in specific columns of a DataFrame.
  
10. **check_regex_pattern(df, string_cols, pattern)**
    - Checks if values in string columns match a specified regex pattern.

## Usage

1. Clone the repository:
    ```
    git clone https://github.com/your_username/data-quality-checks.git
    ```

2. Import the Python script into your project:
    ```python
    from data_quality_checks import *
    ```

3. Apply the desired data quality checks functions to your DataFrame:
    ```python
    # Example usage:
    missing_vals = check_missing_values(my_dataframe)
    print("Missing values:", missing_vals)
    ```

## Contributing

Contributions to this repository are welcome! If you have suggestions for additional data quality checks functions or improvements to existing ones, feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

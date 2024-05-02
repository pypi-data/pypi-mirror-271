# IMS Package Documentation

The IMS package is a python library for processing incoming data into a format that can be used for projects. IMS processing offers a variety of functions to manipulate and analyze data efficiently. Here are the functionalities provided by the package:

### 1. `get_wd_levels(levels)`
- **Description**: Get the working directory with the option of moving up parents.
- **Usage**: `get_wd_levels(levels)`

### 2. `remove_rows(data_frame, num_rows_to_remove)`
- **Description**: Removes a specified number of rows from a pandas DataFrame.
- **Usage**: `remove_rows(data_frame, num_rows_to_remove)`

### 3. `aggregate_daily_to_wc_long(df, date_column, group_columns, sum_columns, wc, aggregation='sum', include_totals=False)`
- **Description**: Aggregates daily data into weekly data, grouping and summing specified columns, starting on a specified day of the week. In the long format.
- **Usage**: `aggregate_daily_to_wc_long(df, date_column, group_columns, sum_columns, wc, aggregation='sum', include_totals=False)`

### 4. `convert_monthly_to_daily(df, date_column)`
- **Description**: Converts monthly data in a DataFrame to daily data by expanding and dividing the numeric values.
- **Usage**: `convert_monthly_to_daily(df, date_column)`

### 5. `plot_two(df1, col1, df2, col2, date_column, same_axis=True)`
- **Description**: Plots specified columns from two different DataFrames using a shared date column. Useful for comparing data.
- **Usage**: `plot_two(df1, col1, df2, col2, date_column, same_axis=True)`

### 6. `remove_nan_rows(df, col_to_remove_rows)`
- **Description**: Removes rows from a DataFrame where the specified column has NaN values.
- **Usage**: `remove_nan_rows(df, col_to_remove_rows)`

### 7. `filter_rows(df, col_to_filter, list_of_filters)`
- **Description**: Filters the DataFrame based on whether the values in a specified column are in a provided list.
- **Usage**: `filter_rows(df, col_to_filter, list_of_filters)`

### 8. `plot_one(df1, col1, date_column)`
- **Description**: Plots a specified column from a DataFrame.
- **Usage**: `plot_one(df1, col1, date_column)`

### 9. `week_of_year_mapping(df, week_col, start_day_str)`
- **Description**: Converts a week column in 'yyyy-Www' or 'yyyy-ww' format to week commencing date.
- **Usage**: `week_of_year_mapping(df, week_col, start_day_str)`

### 10. `exclude_rows(df, col_to_filter, list_of_filters)`
- **Description**: Removes rows from a DataFrame based on whether the values in a specified column are not in a provided list.
- **Usage**: `exclude_rows(df, col_to_filter, list_of_filters)`

### 11. `rename_cols(df, cols_to_rename)`
- **Description**: Renames columns in a pandas DataFrame.
- **Usage**: `rename_cols(df, cols_to_rename)`

### 12. `merge_new_and_old(old_df, old_col, new_df, new_col, cutoff_date, date_col_name='OBS')`
- **Description**: Creates a new DataFrame with two columns: one for dates and one for merged numeric values.
- **Usage**: `merge_new_and_old(old_df, old_col, new_df, new_col, cutoff_date, date_col_name='OBS')`

### 13. `merge_dataframes_on_date(dataframes, common_column='OBS', merge_how='outer')`
- **Description**: Merge a list of DataFrames on a common column.
- **Usage**: `merge_dataframes_on_date(dataframes, common_column='OBS', merge_how='outer')`

### 14. `merge_and_update_dfs(df1, df2, key_column)`
- **Description**: Merges two dataframes on a key column, updates the first dataframe's columns with the second's where available, and returns a dataframe sorted by the key column.
- **Usage**: `merge_and_update_dfs(df1, df2, key_column)`

### 15. `convert_us_to_uk_dates(df, date_col)`
- **Description**: Convert a DataFrame column with mixed date formats to datetime.
- **Usage**: `convert_us_to_uk_dates(df, date_col)`

### 16. `combine_sheets(all_sheets)`
- **Description**: Combines multiple DataFrames from a dictionary into a single DataFrame.
- **Usage**: `combine_sheets({'Sheet1': df1, 'Sheet2': df2})`

### 17. `dynamic_pivot(data_frame, index_col, columns, values_col, fill_value=0)`
- **Description**: Dynamically pivots a DataFrame based on specified columns.
- **Usage**: `dynamic_pivot(df, 'Date', ['Category1', 'Category2'], ['Value1'])`

### 18. `classify_within_column(df, col_name, to_find_dict, default_value = 'other')`
- **Description**: Allows you to map a dictionary of substrings within a column.
- **Usage**: `classify_within_column(df, 'campaign', {'uk_': 'uk'}, 'other')`

### 19. `aggregate_daily_to_wc_wide(df, date_column, group_columns, sum_columns, wc, aggregation='sum', include_totals=False)`
- **Description**: Aggregates daily data into weekly data, grouping and summing specified columns, starting on a specified day of the week. In the wide format.
- **Usage**: `aggregate_daily_to_wc_wide(df, date_column, group_columns, sum_columns, wc, aggregation='sum', include_totals=False)`

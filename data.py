import pandas as pd
import numpy as np

# Sample DataFrame
data = {
    'A': ['1,000', '2,000', '30,000', '45,000'],  # Numeric with commas
    'B': ['25,000', '32,000', '4,000', '20.2'],  # Numeric with commas
    'C': ["this is text, can you check?", 'hello', "Hi, there!", "this is it"],  # Text
    'D': ['twenty', '20', '45', '10'],
    'E': ['2022/01/05', '2022/02/10', '2022/03/15', '2022/04/20'],
    'F': ['50.0085', '20.02', '45.001', 'Forty'],  # Mixed content
    # Mixed content
}
data_frame = pd.DataFrame(data)


def is_numeric(value, number_type=float):
    """Check if a value is numeric (after removing commas)."""
    try:
        number_type(value)
        return True
    except ValueError:
        return False


def clean_and_convert_column(column):
    """Remove commas from values and convert columns based on their content."""
    if column.dtype == 'object':
        # Remove commas from column values
        cleaned_column = column.str.replace(',', '', regex=False)

        # Determine if the column is numeric or text
        numeric_count = cleaned_column.apply(is_numeric).sum()
        total_count = len(cleaned_column)
        string_count = total_count - numeric_count

        # If the majority of values are numeric, convert to numeric
        if numeric_count > string_count:
            # Convert to numeric and handle NaN
            numeric_column = pd.to_numeric(cleaned_column, errors='coerce')
            # Check if all non-NaN values are integers
            if numeric_column.dropna().apply(lambda x: x % 1 == 0).all():
                # loop through each items in numeric_column, convert to NA if not valid integer
                converted = cleaned_column.apply(lambda x: np.nan if not is_numeric(x, int) else x)
            else:
                converted = numeric_column.apply(lambda x: np.nan if not is_numeric(x) else x)
        else:
            converted = column.apply(lambda x: None if is_numeric(x) else x)
        return converted
    else:
        # If the column is not of type object, return it as is
        return column


def convert_column_types(df):
    """Apply conversion to all columns in the DataFrame."""
    for column in df.columns:
        print(df[column].name, df[column].dtypes)
        df[column] = clean_and_convert_column(df[column])
        print(df[column].dtypes, '\n')
    return df


# Apply the conversion function
data_frame_copy = convert_column_types(data_frame.copy())

# Print the modified DataFrame and its types
print("\nModified DataTypes:")
print(data_frame_copy.dtypes)
print("\nModified DataFrame:")
print(data_frame_copy)

# Calculate consistency
total_values = data_frame.size
consistent_values = 0

# Type mapping with only core types
type_mapping = {
    'Int64': int,
    'Float64': float,
    'object': str,
    'bool': bool,
    'datetime64[ns]': pd.Timestamp
}

# Construct schema based on detected types
schema = {column: type_mapping.get(str(dtype), object) for column, dtype in data_frame_copy.dtypes.items()}


def checkinstance(x, t):
    is_instance = isinstance(x, t)
    print(x, t, is_instance)
    return isinstance(x, t)


# count all None values in data_frame_copy as inconstient_values
inconsistent_values = data_frame_copy.isna().sum().sum()
#
# # Calculate consistency of values in terms of their type
# for column in data_frame.columns:
#     if column in schema:
#         column_type = schema[column]
#
#         consistent_values += data_frame_copy.count[column].naapply(lambda x: checkinstance(x, column_type)).sum()

print(f"\nInconsistent: {inconsistent_values}, Total: {total_values}")
consistency = (1 - inconsistent_values / total_values) * 100
# print(f"\nConsistent: {consistent_values}, total: {total_values}")
print(f"\nConsistency: {consistency:.2f}%")

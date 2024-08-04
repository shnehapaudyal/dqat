def calculate_ease_of_manipulation(df):
    # Align the DataFrames to ensure they have identical indices and columns
    cleaned_df = df.dropna()
    df, cleaned_df = df.align(cleaned_df, join='outer', fill_value=float('nan'))
    differences = (df != cleaned_df).sum().sum()
    total_values = df.size
    ease_of_manipulation = (1 - differences / total_values) * 100
    return ease_of_manipulation


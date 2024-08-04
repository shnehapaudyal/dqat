def calculate_uniqueness(df):
    total_rows = len(df)
    unique_rows = len(df.drop_duplicates())
    uniqueness = (unique_rows / total_rows) * 100
    return uniqueness


def duplicate_records(df):
    # Calculate the number of duplicate records
    duplicate_records_count = int(df.duplicated().sum())

    # Calculate the percentage of duplicate records
    duplicate_records_percentage = float((duplicate_records_count / len(df)) * 100)

    return {
        "duplicate_records_count": duplicate_records_count,
        "duplicate_records_percentage": duplicate_records_percentage
    }

def calculate_completeness(df):
    total_values = df.size
    non_empty_values = df.notna().sum().sum()

    completeness = (non_empty_values / total_values) * 100
    return completeness


def missingvalues(df):
    try:
        # null = df.isnull().sum().to_dict()
        nullpercentage = ((df.isna().sum() / len(df)) * 100).to_dict()
        return nullpercentage
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

import nltk
from nltk import corpus, tokenize
import pandas as pd

from nltk_utils import download_nltk

download_nltk()


def get_data():
    dataset_path = ["datasets/dementia-death-rates-new.csv", "datasets/Monkeypox Coursework Dataset.csv",
                    "datasets/AppleStore.csv"]
    data_frame = pd.read_csv(dataset_path[1])
    return data_frame


def calculate_completeness(df):
    total_values = df.size
    non_empty_values = df.notna().sum().sum()
    completeness = (non_empty_values / total_values) * 100
    return completeness


def calculate_uniqueness(df):
    total_rows = len(df)
    unique_rows = len(df.drop_duplicates())
    uniqueness = (unique_rows / total_rows) * 100
    return uniqueness


def calculate_consistency(df, schema):
    total_values = df.size
    consistent_values = 0
    for column in df.columns:
        if column in schema:
            consistent_values += df[column].apply(lambda x: isinstance(x, schema[column])).sum()
    consistency = (consistent_values / total_values) * 100
    return consistency


def calculate_conformity(df, formats):
    total_values = df.size
    conforming_values = 0
    for column in df.columns:
        if column in formats:
            conforming_values += df[column].apply(lambda x: bool(formats[column].match(str(x)))).sum()
    conformity = (conforming_values / total_values) * 100
    return conformity


# till here Checked
def calculate_timeliness(df, current_date, last_modification_date, creation_date):
    timeliness = (current_date - last_modification_date) / (current_date - creation_date) * 100
    return timeliness


def calculate_volatility(current_date, creation_date, modification_date):
    volatility = (creation_date - modification_date) / (current_date - creation_date) * 100
    return volatility


# Load English words from NLTK
english_words = set(corpus.words.words())


def calculate_readability(df):
    # Helper function to check if a value is correctly spelled
    def is_correctly_spelled(value):
        if isinstance(value, str):
            tokens = tokenize.word_tokenize(value)
            return all(token.lower() in english_words for token in tokens)
        return True

    total_values = df.size

    processed_values = df.map(lambda x: isinstance(x, (str, int, float)) and is_correctly_spelled(x)).sum().sum()
    readability = (processed_values / total_values) * 100
    return readability


def calculate_ease_of_manipulation(df):
    # Align the DataFrames to ensure they have identical indices and columns
    cleaned_df = df.dropna()
    df, cleaned_df = df.align(cleaned_df, join='outer', fill_value=float('nan'))
    differences = (df != cleaned_df).sum().sum()
    total_values = df.size
    ease_of_manipulation = (differences / total_values) * 100
    return ease_of_manipulation


def calculate_relevancy(access_count, total_access_count):
    relevancy = (access_count / total_access_count) * 100
    return relevancy


def calculate_security(policy, protocols, threat_detection, encryption, documentation):
    security = sum([policy, protocols, threat_detection, encryption, documentation]) / 5 * 100
    return security


def calculate_accessibility(df):
    total_values = df.size
    accessible_values = df.notna().sum().sum()  # Simplified assumption
    accessibility = (accessible_values / total_values) * 100
    return accessibility


def calculate_integrity(df):
    processed_df = df.dropna();
    df, processed_df = df.align(processed_df, join='outer', fill_value=float('nan'))
    integrity_differences = (df != processed_df).sum().sum()
    total_values_1 = df.size
    integrity = ((total_values_1 - integrity_differences) / total_values_1) * 100
    return integrity


if __name__ == "__main__":
    # Example usage
    df = get_data()
    consistent_values = 0
    type_mapping = {
        'int64': int,
        'float64': float,
        'object': str,
        'bool': bool,
        'datetime64[ns]': pd.Timestamp
    }
    schema = {column: type_mapping[str(dtype)] for column, dtype in df.dtypes.items()}
    formats = {"date": r"\d{4}-\d{2}-\d{2}",
               "time": r"\b([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\b",
               "email": r"[^@]+@[^@]+\.[^@]+",
               "zip_code": r"\b\d{5}\b",
               "credit_card": r"\b\d{4}-?\d{4}-?\d{4}-?\d{4}\b",
               "url": r"https?://[^\s]+",
               "uk_postal_code": r"^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$",
               "canadian_postal_code": r"^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$"
               }
    current_date = pd.Timestamp.now()
    last_modification_date = pd.Timestamp("2023-06-01")
    creation_date = pd.Timestamp("2022-01-01")
    access_count = 150
    total_access_count = 200
    policy = True
    protocols = True
    threat_detection = True
    encryption = True
    documentation = True
    original_df = df.copy()
    processed_df = df.copy()  # Assume some preprocessing has been done

    completeness = calculate_completeness(df)
    uniqueness = calculate_uniqueness(df)
    consistency = calculate_consistency(df, schema)
    conformity = calculate_conformity(df, formats)
    timeliness = calculate_timeliness(df, current_date, last_modification_date, creation_date)
    volatility = calculate_volatility(current_date, creation_date, last_modification_date)
    readability = calculate_readability(df)
    ease_of_manipulation = calculate_ease_of_manipulation(df)
    relevancy = calculate_relevancy(access_count, total_access_count)
    security = calculate_security(policy, protocols, threat_detection, encryption, documentation)
    accessibility = calculate_accessibility(df)
    integrity = calculate_integrity(df)

    print(f"Completeness: {completeness}%")
    print(f"Uniqueness: {uniqueness}%")
    print(f"Consistency: {consistency}%")
    print(f"Conformity: {conformity}%")
    print(f"Timeliness: {timeliness}%")
    print(f"Volatility: {volatility}%")
    print(f"Readability: {readability}%")
    print(f"Ease of Manipulation: {ease_of_manipulation}%")
    print(f"Relevancy: {relevancy}%")
    print(f"Security: {security}%")
    print(f"Accessibility: {accessibility}%")
    print(f"Integrity: {integrity}%")
    # print(f"Score: {score}%")

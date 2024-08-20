from spellchecker import SpellChecker
import contractions
import re

from domain.consistency import is_numeric

spell = SpellChecker()


def preprocess_text(text):
    # Expand contractions
    text = contractions.fix(text)

    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-z\s]', '', text)

    return text


def is_correctly_spelled(value):
    if isinstance(value, str):
        processed_text = preprocess_text(value)
        misspelled = spell.unknown(spell.split_words(processed_text))
        return len(misspelled) == 0
    return True


def calculate_readability(df, type_info):
    # Helper function to check if a value is correctly spelled
    data_types, column_types, consistency_values = type_info

    columns = column_types[column_types['type'] == 'string']['column']
    if len(columns) == 0:
        return 100

    df_filtered = df[columns]
    total_values = df_filtered.size

    df_map = df_filtered.map(lambda x: is_correctly_spelled(x))
    correctly_spelled_values = df_map.sum().sum()
    readability = (correctly_spelled_values / total_values) * 100
    return readability


def typos(df, type_info):
    # Function to calculate readability scores, counts, and typo percentages
    typo_percentages = {}

    data_types, column_types, consistency_values = type_info
    columns = column_types[column_types['type'] == 'string']['column']

    def typo(column):
        correctly_spelled = df[column].map(lambda x: is_correctly_spelled(x)).sum()
        total_count = len(df[column])
        return ((total_count - correctly_spelled) / total_count) * 100

    for column in df.columns:
        typo_percentages[column] = typo(column) if column in columns.values else 0

    return typo_percentages

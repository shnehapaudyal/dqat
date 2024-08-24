import nltk.corpus
import pandas as pd
from spellchecker import SpellChecker
import contractions
import re
from nltk.corpus import wordnet

from domain.consistency import is_numeric

spell = SpellChecker()
spell.word_frequency.load_words(wordnet.words())

def preprocess_text(text):
    # Expand contractions
    text = contractions.fix(text)

    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-z\s]', '', text)

    return text


def is_correctly_spelled(value):
    processed_text = preprocess_text(str(value))
    misspelled = spell.unknown(spell.split_words(processed_text))
    return len(misspelled) == 0


def calculate_readability(df, type_info):
    # Helper function to check if a value is correctly spelled
    data_types, column_types, consistency_values = type_info

    string_columns = pd.concat(
        (column_types[column_types['type'] == 'string']['column'],
         column_types[column_types['type'] == 'enum']['column'])
    ).values

    if len(string_columns) == 0:
        return None

    correctly_spelled_sum = df[string_columns].map(lambda x: is_correctly_spelled(x)).sum().sum()

    total_values = df[string_columns].size

    readability = (correctly_spelled_sum / total_values) * 100
    return readability


def typos(df, type_info):
    # Function to calculate readability scores, counts, and typo percentages
    typo_percentages = {}

    data_types, column_types, consistency_values = type_info
    string_columns = pd.concat(
        (column_types[column_types['type'] == 'string']['column'],
         column_types[column_types['type'] == 'enum']['column'])
    ).values

    def typo(column):
        correctly_spelled = df[column].map(lambda x: is_correctly_spelled(x)).sum()
        total_count = len(df[column])
        return ((total_count - correctly_spelled) / total_count) * 100

    for column in df.columns:
        typo_percentages[column] = typo(column) if column in string_columns else 0

    return typo_percentages

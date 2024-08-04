import nltk
from nltk.corpus import wordnet

from domain.consistency import is_numeric

nltk.download('words')
nltk.download('punkt')
from nltk_utils import download_nltk
from nltk import corpus, tokenize

download_nltk()

# Load English words from NLTK
# english_words = {eng.lower() for eng in set(corpus.words.words('en'))}


def is_text(value):
    return isinstance(value, str) and not is_numeric(value)


def is_correctly_spelled(value):
    if isinstance(value, str):
        tokens = tokenize.word_tokenize(value)
        return all(wordnet.synsets(token) for token in tokens)
    return True


def calculate_readability(df):
    # Helper function to check if a value is correctly spelled
    total_values = df.size
    df_map = df.map(lambda x: not is_text(x) or is_correctly_spelled(x))
    df.to_dict()
    correctly_spelled_values = df_map.sum().sum()
    readability = (correctly_spelled_values / total_values) * 100
    return readability


def typos(df):
    # Function to calculate readability scores, counts, and typo percentages
    typo_percentages = {}

    for column in df.columns:
        correctly_spelled = df[column].map(lambda x: not is_text(x) or is_correctly_spelled(x)).sum()
        total_count = len(df[column])
        typo_percentages[column] = ((total_count - correctly_spelled) / total_count) * 100

    return typo_percentages

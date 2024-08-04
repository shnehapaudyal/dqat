import nltk
nltk.download('words')
nltk.download('punkt')
from nltk.corpus import words
from nltk_utils import download_nltk
from nltk import corpus, tokenize
from nltk.tokenize import word_tokenize
download_nltk()


# Load English words from NLTK
english_words = set(corpus.words.words())


def is_correctly_spelled(value):
    if isinstance(value, str):
        tokens = tokenize.word_tokenize(value)
        return all(token.lower() in english_words for token in tokens)
    return True


def calculate_readability(df):
    # Helper function to check if a value is correctly spelled
    total_values = df.size
    processed_values = df.map(lambda x: isinstance(x, (str, int, float)) and is_correctly_spelled(x)).sum().sum()
    readability = (1 - processed_values / total_values) * 100
    return readability


def typos(df):
    # Function to calculate readability scores, counts, and typo percentages
    typo_percentages = {}

    for column in df.columns:
        correctly_spelled = df[column].apply(is_correctly_spelled).sum()
        total_count = len(df[column])
        typo_percentages[column] = ((total_count - correctly_spelled) / total_count) * 100

    return typo_percentages
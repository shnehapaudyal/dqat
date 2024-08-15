import pickle
import re

import pandas as pd
import syllapy


def compute_features(text_series):
    """Compute features for text quality analysis."""
    features_list = []

    for text in text_series:
        # Tokenize the text into sentences and words
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        words = [word for sentence in sentences for word in sentence.split()]

        # Calculate features
        unique_words = len(set(words))
        total_words = len(words)
        syllable_count = sum(syllapy.count(word) for word in words)
        total_sentences = len(sentences)

        # Calculate ratios and handle potential division by zero
        unique_words_ratio = unique_words / total_words if total_words > 0 else 0

        # Append computed features to the list
        features_list.append({
            'unique_words_ratio': unique_words_ratio,
            'average_sentence_length': total_sentences,
            'total_words': total_words,
            'syllable_count': syllable_count,
        })

    # Convert the list of dictionaries to a DataFrame
    features_df = pd.DataFrame(features_list).fillna(0)
    return features_df


def get_rfl(values):
    with open('model/rfc.pkl', 'rb') as f:
        rfl_model = pickle.load(f)
    features = compute_features(values)
    try:
        predicted = rfl_model.predict(features)
        return predicted
    except Exception as e:
        print(f"Error in get_rfl: {e}")
        raise e

import db
from files import files
from domain import diversity, ease_of_manipulation
from domain import outlier, types, completeness, readability, conformity, consistency, uniqueness


def get_dataset_metrics(df):
    return dataset_metrics(df)


def dataset_metrics(df):
    type_info = types.get_type_info(df)

    return [
        {'name': 'completeness', 'score': completeness.calculate_completeness(df)},
        {'name': 'uniqueness', 'score': uniqueness.calculate_uniqueness(df)},
        {'name': 'consistency', 'score': consistency.calculate_consistency(df, type_info)},
        {'name': 'conformity', 'score': conformity.calculate_conformity(df, types.supported_patterns, type_info)},
        {'name': 'readability', 'score': readability.calculate_readability(df, type_info)},
        {'name': 'ease_of_manipulation', 'score': ease_of_manipulation.calculate_ease_of_manipulation(df)},
        {'name': 'lexical_diversity', 'score': diversity.calculate_diversity(df, type_info)},
    ]


def get_dataset_dataframe(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = files.read(dataset_path)
    return df


def calculate_overall_score(df):
    metrics = dataset_metrics(df)

    total_score = sum(metric['score'] for metric in metrics)

    return total_score / len(metrics)


def get_missingvalue(df):
    return completeness.missingvalues(df)


def get_inconsistent_datatype(df):
    type_info = types.get_type_info(df)
    return consistency.inconsistency(df, type_info)


def get_outlier(df):
    type_info = types.get_type_info(df)
    return outlier.outliers(df, type_info)


def get_typos(df):
    type_info = types.get_type_info(df)
    return readability.typos(df, type_info)


def get_invalid_formats(df):
    type_info = types.get_type_info(df)
    return conformity.invalid_formats(df, types.supported_patterns, type_info)


def get_duplicate(df):
    return {}
    # duplicates_info = definemetrics.duplicate_records(df)
    # duplicates_info = {key: float(value) if isinstance(value, (int, float)) else value for key, value in
    #                    duplicates_info.items()}
    # return jsonify(duplicates_info)

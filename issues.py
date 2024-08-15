from domain import outlier, types, completeness, readability, conformity, consistency


def get_issues_list():
    return [
        'missing_values',
        'inconsistency',
        'outliers',
        'typo',
        'invalid_format',
        # 'duplicate',
    ]


def dataset_issues(df):
    type_info = types.get_type_info(df)

    issues = [
        {'name': 'missing_values', 'value': completeness.missingvalues(df)},
        {'name': 'inconsistency', 'value': consistency.inconsistency(df, type_info)},
        {'name': 'outliers', 'value': outlier.outliers(df, type_info)},
        {'name': 'typo', 'value': readability.typos(df, type_info)},
        {'name': 'invalid_format', 'value': conformity.invalid_formats(df, types.supported_patterns, type_info)},
    ]

    return issues

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

    issues = {
        'missing_values': completeness.missingvalues(df),
        'inconsistency': consistency.inconsistency(df, type_info),
        'outliers': outlier.outliers(df, type_info),
        'typo': readability.typos(df, type_info),
        'invalid_format': conformity.invalid_formats(df, types.supported_patterns, type_info),
    }

    return issues

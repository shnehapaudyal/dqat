from pathlib import Path
from nltk import download as nltk_download
from typing import List


def download_nltk_data(
        list_of_resources: List[str],
) -> None:
    for resource in list_of_resources:
        nltk_download(
            info_or_id=resource,
            # quiet=True,  # Change this if you wanna suppress the message
        )


def download_nltk():
    download_nltk_data(
        list_of_resources=[
            'words',
            'wordnet',
            'stopwords',
            'punkt',
        ],
    )

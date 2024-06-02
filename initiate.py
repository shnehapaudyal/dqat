import pandas as pd


def get_data():
    dataset_path = ["datasets\dementia-death-rates new.csv", "datasets\AppleStore.csv"]
    df = pd.read_csv(dataset_path[1])
    return df
def metrics():




print(get_data())

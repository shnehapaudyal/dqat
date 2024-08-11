import pandas as pd

schema = {"column1": int, "column2": str}  # Define your schema
formats = {"date1": r"\d{4}-\d{2}-\d{2}",
           "date2": r"\d{2}-\d{2}-\d{4}",
           "time": r"\b([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\b",
           "email": r"[^@]+@[^@]+\.[^@]+",
           "zip_code": r"\b\d{5}\b",
           "credit_card": r"\b\d{4}-?\d{4}-?\d{4}-?\d{4}\b",
           "url": r"[a-z]*+://[^\s]+",
           "uk_postal_code": r"^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$",
           "canadian_postal_code": r"^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$",
           }  # Define your formats
current_date = pd.Timestamp.now()
last_modification_date = pd.Timestamp("2023-06-01")
creation_date = pd.Timestamp("2022-01-01")
access_count = 150
total_access_count = 200
policy = True
protocols = True
threat_detection = True
encryption = True
documentation = True

supported_formats = {
    r"\d{4}-\d{2}-\d{2}",
    r"\d{2}-\d{2}-\d{4}",
    r"\b([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\b",
    r"[^@]+@[^@]+\.[^@]+",
    r"\b\d{5}\b",
    r"\b\d{4}-?\d{4}-?\d{4}-?\d{4}\b",
    r"https?://[^\s]+",
    r"^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$",
    r"^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$",
}

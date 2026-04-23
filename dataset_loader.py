import pandas as pd

df = pd.read_csv("dataset_small.csv")


def search_by_symptoms(user_input):
    results = []

    for _, row in df.iterrows():
        disease = row["Disease"]
        text = str(row.values).lower()

        if any(word in text for word in user_input.lower().split()):
            results.append(disease)

    if not results:
        return "No matching diseases found."

    return "\n".join(results[:5])
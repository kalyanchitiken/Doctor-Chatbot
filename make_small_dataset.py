import pandas as pd

# load big dataset
df = pd.read_csv("Final_Augmented_dataset_Diseases_and_Symptoms.csv")

# take only 5000 rows (you can change number)
df_small = df.sample(5000)

# save smaller file
df_small.to_csv("dataset_small.csv", index=False)

print("✅ Small dataset created: dataset_small.csv")
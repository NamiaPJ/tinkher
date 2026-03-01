import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

np.random.seed(42)

data = []

for _ in range(400):
    leafy = np.random.randint(0, 7)
    fruits = np.random.randint(0, 7)
    milk = np.random.randint(0, 7)
    eggs = np.random.randint(0, 7)
    meat = np.random.randint(0, 7)
    pulses = np.random.randint(0, 7)
    sunlight = np.random.randint(0, 30)

    # Individual deficiency logic
    iron_def = 1 if leafy < 3 else 0
    calcium_def = 1 if milk < 3 else 0
    vitaminD_def = 1 if sunlight < 15 else 0
    protein_def = 1 if (eggs + meat + pulses) < 5 else 0

    data.append([
        leafy, fruits, milk, eggs, meat, pulses, sunlight,
        iron_def, calcium_def, vitaminD_def, protein_def
    ])

columns = [
    "leafy", "fruits", "milk", "eggs", "meat", "pulses", "sunlight",
    "iron_def", "calcium_def", "vitaminD_def", "protein_def"
]

df = pd.DataFrame(data, columns=columns)

X = df[["leafy", "fruits", "milk", "eggs", "meat", "pulses", "sunlight"]]
y = df[["iron_def", "calcium_def", "vitaminD_def", "protein_def"]]

model = RandomForestClassifier()
model.fit(X, y)

os.makedirs("model", exist_ok=True)
pickle.dump(model, open("model/nutrition_model.pkl", "wb"))

print("Multi-deficiency model trained successfully!")
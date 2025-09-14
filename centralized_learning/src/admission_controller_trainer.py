import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

# Load data
df = pd.read_csv("prototype1_data_from_postgress-1749474919331.csv")
df['slice'] = np.where(df['upf'] == "upf500", 1, 2)
print (df.head())

# Select features
features = ["active_ues", "slice1_active_ues", "slice2_active_ues", "slice"]
X = df[features].values
y = df["admission_flag"].values

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# # Build model
# model = tf.keras.Sequential([
#     tf.keras.layers.Dense(16, activation='relu', input_shape=(len(features),)),
#     tf.keras.layers.Dense(8, activation='relu'),
#     tf.keras.layers.Dense(1, activation='sigmoid')
# ])


# Build model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=1000, batch_size=4, verbose=0)

# Save model and scaler
model.save("ue_admission_model.h5")
import joblib
joblib.dump(scaler, "ue_admission_scaler.pkl")

# Evaluate
loss, acc = model.evaluate(X_test, y_test)
print(f"Test accuracy: {acc:.2f}")


import tensorflow as tf
import joblib
import numpy as np

# Load model and scaler
model = tf.keras.models.load_model("ue_admission_model.h5")
scaler = joblib.load("ue_admission_scaler.pkl")

def predict_admission(ue_features):
    # ue_features = [active ues, slice1_active_ues, slice2_active_ues, slice]
    X = scaler.transform([ue_features])
    prob = model.predict(X)[0][0]
    print(prob)
    return prob >= 0.5

# Example input
ue_input = [3, 3, 6, 1]
if predict_admission(ue_input):
    print("Admit UE")
else:
    print("Deny UE")

ue_input = [3, 3, 6, 2]
if predict_admission(ue_input):
    print("Admit UE")
else:
    print("Deny UE")



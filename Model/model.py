import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from scipy.sparse import hstack

# 1️⃣ Load Data
file_path = "user_4.xlsx"  # Change this to your xlsx file
df = pd.read_excel(file_path)

# 2️⃣ Preprocessing
def clean_text(text):
    if isinstance(text, str):
        return re.sub(r'\W+', ' ', text.lower())  # Remove special chars
    return ""

df["Processed_CV"] = df["CV"].astype(str).apply(clean_text)
df["Processed_Info"] = df["Moreinfo"].astype(str).apply(clean_text)

# Combine relevant columns
df["Full_Text"] = df["Processed_CV"] + " " + df["Processed_Info"]
df["Experience_Years"] = df["Experience Years"].fillna(0)
df["English_Level"] = df["English Level"].fillna(0)

# 3️⃣ Convert Text to Vectors (TF-IDF)
vectorizer = TfidfVectorizer(max_features=300, sublinear_tf=True)
X_text = vectorizer.fit_transform(df["Full_Text"])  # Keep sparse format

# 4️⃣ Combine Features (Sparse Matrix)
X = hstack((X_text, df[["Experience_Years", "English_Level"]].values))

# 5️⃣ Labels (Simulated Scores for now)
df["Score"] = np.random.uniform(0, 10, len(df))  # Generate dummy scores
y = df["Score"]

# 6️⃣ Train-Test Split (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7️⃣ Train Model
model = RandomForestRegressor(n_estimators=50, n_jobs=-1, random_state=42)
model.fit(X_train, y_train)

# 8️⃣ Test Model
y_pred = model.predict(X_test)

# 9️⃣ Evaluate Performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"✅ Model Evaluation:")
print(f"Mean Squared Error: {mse:.2f}")
print(f"R² Score: {r2:.2f}")

# 10️⃣ Predict New Resume Score
def predict_resume(resume_text, experience, english_level):
    processed_text = clean_text(resume_text)
    vectorized_text = vectorizer.transform([processed_text])  # Keep sparse
    new_X = hstack((vectorized_text, [[experience, english_level]]))
    score = model.predict(new_X)[0]
    return round(score, 2)

# Example Prediction
new_resume = "Experienced customer support with 3 years of experience, problem-solving, communication, tech support."
predicted_score = predict_resume(new_resume, experience=3, english_level=3)
print(f"Predicted Resume Score: {predicted_score}/10")

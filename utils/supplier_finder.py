import pandas as pd
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from tensorflow import keras
import pickle

# Load vectorizer and label encoder
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Load the saved Keras model
product_model = keras.models.load_model("checkpoints/best_model_run_10.keras")

def clean_text(text):
    stopwords = ENGLISH_STOP_WORDS
    words = re.findall(r'\b\w+\b', str(text).lower())
    return [word for word in words if word not in stopwords]

def find_suppliers(text, df, vectorizer, product_model, label_encoder):
    user_words = clean_text(text)
    if not user_words:
        return pd.DataFrame(columns=["Supplier/Vendor", "Item Description", "Product Name", "PO Amount"])

    vectorized_input = vectorizer.transform([' '.join(user_words)])
    
    prediction_probs = product_model.predict(vectorized_input.toarray())
    pred_class = prediction_probs.argmax()
    predicted_product = label_encoder.inverse_transform([pred_class])[0]

    product_matches = df[df["Product Name"].str.lower() == predicted_product.lower()]

    def match_keywords(desc):
        desc_words = re.findall(r'\b\w+\b', str(desc).lower())
        return any(word in desc_words for word in user_words)

    keyword_matches = df[df["Item Description"].apply(match_keywords)]

    combined = pd.concat([product_matches, keyword_matches], ignore_index=True)
    combined = combined.drop_duplicates(subset=["Supplier/Vendor", "Item Description"])

    def has_keyword(desc, user_words):
        desc_words = re.findall(r'\b\w+\b', str(desc).lower())
        return int(any(word in desc_words for word in user_words))

    # Score based only on keywords present in Item Description
    combined['score'] = combined.apply(
        lambda row: has_keyword(row["Item Description"], user_words),
        axis=1
    )

    combined = combined.sort_values(by='score', ascending=False).drop(columns='score').reset_index(drop=True)

    return combined[["Supplier/Vendor", "Item Description", "Product Name", "PO Amount"]]

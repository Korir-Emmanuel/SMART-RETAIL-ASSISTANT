import pandas as pd
import re
import joblib
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from tensorflow import keras
import pickle

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

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
    
    # Use model.predict on the numpy array input (as you saved it)
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

    return combined[["Supplier/Vendor", "Item Description", "Product Name", "PO Amount"]]

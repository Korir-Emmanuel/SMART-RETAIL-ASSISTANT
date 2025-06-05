import streamlit as st
import pandas as pd
import altair as alt
from utils.nlp_classifier import classify_intent
from utils.supplier_finder import find_suppliers
from utils.spending_parser import parse_spending_query
import streamlit.components.v1 as components
import pickle
from tensorflow import keras

# Load vectorizer and label encoder
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Load model
product_model = keras.models.load_model("checkpoints/best_model_run_10.keras")


st.set_page_config(layout="wide")
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Load data
def load_data():
    try:
        df = pd.read_excel("Data/data.xlsx")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# Ensure required columns are present
required_columns = {"Item Description", "Product Name", "PO Amount", "Month"}
if not required_columns.issubset(df.columns):
    st.error("Some required columns are missing from the dataset.")

# Session state
if "history" not in st.session_state:
    st.session_state["history"] = []

# Render chat UI
def render_chat(history):
    chat_html = """
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <div class="bg-gray-900 min-h-screen p-4 text-white font-sans">
        <h1 class="text-3xl font-bold text-green-500 mb-6">Spend Optimizer</h1>
        <div class="space-y-4">
    """
    for entry in history:
        if entry["role"] == "user":
            chat_html += f"""
            <div class="flex justify-end">
                <div class="bg-white text-black rounded-xl px-4 py-2 max-w-md shadow">{entry['content']}</div>
            </div>
            """
        elif entry["role"] == "bot":
            chat_html += f"""
            <div class="flex justify-start">
                <div class="bg-green-500 text-white rounded-xl px-4 py-2 max-w-md shadow">{entry['content']}</div>
            </div>
            """
        elif entry["role"] == "table":
            chat_html += """
            <div class="flex justify-start">
                <div class="bg-green-600 text-white rounded-xl px-4 py-2 max-w-md shadow">[Table shown below]</div>
            </div>
            """
        elif entry["role"] == "chart":
            chat_html += """
            <div class="flex justify-start">
                <div class="bg-green-600 text-white rounded-xl px-4 py-2 max-w-md shadow">[Chart shown below]</div>
            </div>
            """
    chat_html += "</div></div>"
    components.html(chat_html, height=600, scrolling=True)

# Initial welcome message
if not st.session_state.history:
    st.session_state.history.append({"role": "bot", "content": "\U0001F44B Hi there! Ask me anything about spending or suppliers."})

# Chat input
user_input = st.chat_input("Ask me anything about spending and procurement")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})

    with st.spinner("Analyzing your input..."):
        intent, corrected_text, filtered_words = classify_intent(user_input)
        month_filter = None
        data = df.copy()

        if intent == "supplier_query":
            suppliers = find_suppliers(' '.join(filtered_words), data, vectorizer, product_model, label_encoder)
            if not suppliers.empty:
                st.session_state.history.append({"role": "bot", "content": "Here are the matching suppliers:"})
                st.session_state.history.append({"role": "table", "content": suppliers})
            else:
                st.session_state.history.append({"role": "bot", "content": "No matching suppliers found."})

        elif intent == "dashboard":
            group_by, month_filter = parse_spending_query(corrected_text)
            if month_filter:
                data = data[data["Month"].str.contains(month_filter, case=False)]
            grouped = data.groupby(group_by)["PO Amount"].sum().reset_index()
            st.session_state.history.append({"role": "bot", "content": f"Spending grouped by **{group_by}**"})
            st.session_state.history.append({"role": "chart", "content": grouped, "x": group_by})

        else:
            st.session_state.history.append({"role": "bot", "content": "Sorry, I couldn't understand. Try asking about suppliers or spending."})

# Reset option
if st.button("Reset Chat"):
    st.session_state.history = []
    st.rerun()

# Render the chat UI
render_chat(st.session_state.history)

# Show tables & charts
for i, entry in enumerate(st.session_state.history):
    if entry["role"] == "table":
        st.dataframe(entry["content"])
        st.download_button(
            label="Download Results",
            data=entry["content"].to_csv(index=False),
            file_name="supplier_results.csv",
            mime="text/csv",
            key=f"download-{i}"
        )
    elif entry["role"] == "chart":
        chart = alt.Chart(entry["content"]).mark_bar().encode(
            x=alt.X(entry["x"], title=entry["x"].replace("_", " ").title()),
            y=alt.Y("PO Amount", title="Total PO Amount"),
            tooltip=["PO Amount"]
        ).properties(height=400)
        st.altair_chart(chart, use_container_width=True)

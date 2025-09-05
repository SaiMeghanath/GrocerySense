import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="GrocerySense", page_icon="🛒")

st.title("🛒 GrocerySense – Smart Reorder Assistant")
st.write("Predict when you’ll run out of groceries and get reminders!")

if "groceries" not in st.session_state:
    st.session_state.groceries = pd.DataFrame({
        "Item": ["Milk", "Eggs", "Rice", "Tomatoes"],
        "Last Bought": [datetime.now()-timedelta(days=2),
                        datetime.now()-timedelta(days=5),
                        datetime.now()-timedelta(days=15),
                        datetime.now()-timedelta(days=3)],
        "Frequency (days)": [3, 7, 30, 5]
    })

df = st.session_state.groceries

st.subheader("📦 Your Items")
st.dataframe(df)

st.subheader("🔮 Predicted Reminders")
today = datetime.now()
for _, row in df.iterrows():
    next_due = row["Last Bought"] + timedelta(days=row["Frequency (days)"])
    if next_due <= today:
        st.error(f"⚠️ {row['Item']} might be finished! Reorder now.")
    else:
        st.success(f"✅ {row['Item']} is fine. Next reminder: {next_due.date()}")

st.subheader("➕ Add New Item")
item = st.text_input("Item name")
freq = st.number_input("Reorder frequency (days)", min_value=1, max_value=60, value=7)

if st.button("Add Item"):
    new_row = {"Item": item, "Last Bought": today, "Frequency (days)": freq}
    st.session_state.groceries = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    st.success(f"{item} added!")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

DATA_FILE = "portfolio.json"

# بارگذاری داده‌ها
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
        except:
            data = []
else:
    data = []

st.title("📊 Portfolio Tracker")

# فرم افزودن معامله
with st.form("add_trade"):
    name = st.text_input("Name")
    buy_price = st.number_input("Buy Price", value=0.0)
    sell_price = st.number_input("Sell Price", value=0.0)
    submit = st.form_submit_button("➕ Add Trade")

if submit and name:
    trade = {
        "Name": name,
        "Buy": buy_price,
        "Sell": sell_price,
        "Profit": sell_price - buy_price
    }
    data.append(trade)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# نمایش جدول
if data:
    df = pd.DataFrame(data)
    st.dataframe(df)

    # نمودار سود/ضرر
    fig, ax = plt.subplots()
    df["Profit"].plot(kind="bar", ax=ax)
    st.pyplot(fig)
else:
    st.info("هنوز هیچ معامله‌ای ثبت نشده.")

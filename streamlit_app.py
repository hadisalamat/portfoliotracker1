import streamlit as st
import pandas as pd
import json
import os

DATA_FILE = "trades.json"
PAGE_SIZE = 20

# --- بارگذاری و ذخیره ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- داده‌ها ---
trades = load_data()
initial_balance = 2000.0
current_page = st.session_state.get("page", 0)

# --- عنوان ---
st.title("💰 Portfolio Tracker")
st.markdown("<h3 style='color:#27ae60;'>💵 Current Balance: ${:.2f}</h3>".format(
    initial_balance + sum([t.get("profit_loss",0) for t in trades])), unsafe_allow_html=True)

# --- فرم اضافه کردن معامله ---
with st.expander("➕ Add Transaction"):
    name = st.text_input("Name")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    buy_price = st.number_input("Buy Price $", min_value=0.0, step=0.01)
    sell_price = st.number_input("Sell Price $", min_value=0.0, step=0.01)
    if st.button("Add Transaction"):
        profit_loss = round(sell_price - buy_price,2)
        status = "Profit" if profit_loss>=0 else "Loss"
        trades.append({
            "name": name,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "buy_price": buy_price,
            "sell_price": sell_price,
            "profit_loss": profit_loss,
            "status": status
        })
        save_data(trades)
        st.success("Transaction added!")

# --- صفحه‌بندی ---
total_pages = (len(trades)-1)//PAGE_SIZE + 1
start_idx = current_page * PAGE_SIZE
end_idx = start_idx + PAGE_SIZE
page_trades = trades[start_idx:end_idx]

df = pd.DataFrame(page_trades)
st.dataframe(df, use_container_width=True)

col1,col2 = st.columns(2)
if col1.button("Previous") and current_page>0:
    st.session_state.page = current_page-1
    st.experimental_rerun()
if col2.button("Next") and current_page < total_pages-1:
    st.session_state.page = current_page+1
    st.experimental_rerun()

# --- خلاصه ---
total_profit = sum([t["profit_loss"] for t in trades if t["profit_loss"]>0])
total_loss = -sum([t["profit_loss"] for t in trades if t["profit_loss"]<0])
st.markdown(f"💰 Total Profit: ${total_profit:.2f}    ❌ Total Loss: ${total_loss:.2f}")

# --- نمودار پیشرفت ---
import matplotlib.pyplot as plt

balance = initial_balance
balances = []
for t in trades:
    balance += t["profit_loss"]
    balances.append(balance)

fig, ax = plt.subplots()
ax.plot(range(1,len(balances)+1), balances, marker='o', linestyle='-', color='#f1c40f')
ax.set_title("Portfolio Progress", color='white')
ax.set_xlabel("Transaction", color='white')
ax.set_ylabel("Balance $", color='white')
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_facecolor('#1c1c1c')
fig.patch.set_facecolor('#1c1c1c')
ax.tick_params(colors='white')

st.pyplot(fig)

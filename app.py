# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. ส่วนของฟังก์ชัน (Logic) ---
# ฟังก์ชันคำนวณความมั่งคั่งสุทธิ
def calculate_net_worth(assets_df, liabs_df):
    total_a = assets_df["มูลค่า"].sum()
    total_l = liabs_df["มูลค่า"].sum()
    return total_a, total_l, total_a - total_l

# ฟังก์ชันคำนวณสัดส่วนเป็นเปอร์เซ็นต์
def get_asset_allocation(df):
    total = df["มูลค่า"].sum()
    df["สัดส่วน (%)"] = (df["มูลค่า"] / total * 100).round(2)
    return df

# --- 2. การตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="FinPort Pro", page_icon="💰", layout="wide")

# --- 3. ข้อมูลเบื้องต้น ---
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame([
        {"รายการ": "เงินสด", "มูลค่า": 100000, "ประเภท": "Cash"},
        {"รายการ": "หุ้นไทย", "มูลค่า": 500000, "ประเภท": "Equity"}
    ])

if 'liabilities' not in st.session_state:
    st.session_state.liabilities = pd.DataFrame([
        {"รายการ": "หนี้บ้าน", "มูลค่า": 2000000, "ประเภท": "Long-term"}
    ])

# --- 4. การเรียกใช้ฟังก์ชันรับค่า ---
t_assets, t_liabs, net_w = calculate_net_worth(st.session_state.assets, st.session_state.liabilities)
allocation_df = get_asset_allocation(st.session_state.assets)

# --- 5. ส่วนแสดงผล (UI) ---
st.title("🏯 My Financial Treasure Chest")

col1, col2, col3 = st.columns(3)
col1.metric("สินทรัพย์รวม", f"{t_assets:,.0f} ฿")
col2.metric("หนี้สินรวม", f"{t_liabs:,.0f} ฿", delta_color="inverse")
col3.metric("ความมั่งคั่งสุทธิ", f"{net_w:,.0f} ฿")

st.divider()

# ส่วนของกราฟ
c1, c2 = st.columns(2)
with c1:
    st.subheader("📊 สัดส่วนสินทรัพย์ (%)")
    fig = px.pie(allocation_df, values='มูลค่า', names='ประเภท', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("➕ เพิ่มรายการใหม่")
    with st.form("add_form"):
        name = st.text_input("ชื่อรายการ")
        val = st.number_input("มูลค่า (฿)", min_value=0)
        cat = st.selectbox("ประเภท", ["Cash", "Equity", "Alternative"])
        if st.form_submit_button("บันทึกข้อมูล"):
            new_row = pd.DataFrame([{"รายการ": name, "มูลค่า": val, "ประเภท": cat}])
            st.session_state.assets = pd.concat([st.session_state.assets, new_row], ignore_index=True)
            st.rerun()

st.subheader("📋 รายละเอียดสินทรัพย์")
st.table(allocation_df)


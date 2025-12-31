"""
Portfolio Tracker Dashboard
run with streamlit run app.py
"""
import streamlit as st

def main():
    st.set_page_config(
        page_title="Portfolio Tracker",
        page_icon="📈",
        layout="wide",

    )

    st.title("📈 Portfolio Tracker Dashboard")
    st.markdown("Track your investments and monitor your portfolio performance over time.")

if __name__ == "__main__":
    main()
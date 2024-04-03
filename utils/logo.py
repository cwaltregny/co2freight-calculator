import streamlit as st
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://co2freight-calculator.com/wp-content/uploads/2024/02/EcoFreightCalculator_logo-Charlotte-Waltregny.png);
                background-repeat: no-repeat;
                padding-top: 500px;
                background-position: 5px 5px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "CO2 Freight Calculator";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
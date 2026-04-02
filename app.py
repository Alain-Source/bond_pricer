import streamlit as st
import numpy as np
from bond import Bond

# App Title & Sub-title
st.title("Bond Price Calculator")
st.markdown("""An interactive learning tool for exploring fixed-income fundamentals.
Calculate bond prices, yields, and risk measures. 
Visualise how bond prices respond to changes in yield rates.""", unsafe_allow_html=True)

# Setup Tabs
tab1, tab2 = st.tabs(["Calculator", "Visualizer"])

# Calculator Tab
with tab1:
    st.write("Bond Contract")
    col1, col2 = st.columns(2)
    
    with col1:
        face_value = st.number_input("Face Value (R)", value=1000)
        coupon_rate = st.number_input("Coupon Rate", value=0.05)
        maturity = st.number_input("Maturity (years)", value=10)

    with col2:
        frequency = st.number_input("Frequency", value=1)
        yield_rate = st.number_input("Yield Rate", value=0.05)

    if st.button("Calculate"):
        bond = Bond(face_value, coupon_rate, maturity, frequency)
        st.write(f"Bond Price: R {bond.price(yield_rate):.2f}")

# Relationship Visuali  zation Tab
with tab2:
    st.write("In Development")



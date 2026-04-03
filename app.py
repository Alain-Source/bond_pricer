import streamlit as st
import numpy as np
from bond import Bond

# App Title & Sub-title
st.title("Bond Price Calculator")
st.markdown("""An interactive learning tool for exploring fixed-income fundamentals.
<br>Calculate bond prices, yields, and risk measures. 
Visualise bond prices responding to changes in yield rates.""", unsafe_allow_html=True)

# Setup Tabs
tab1, tab2 = st.tabs(["Calculator", "Visualizer"])

# Calculator Tab
with tab1:
    with st.container(border=True):
        st.subheader("Bond Contract")
        
        col1, col2 = st.columns(2)
        with col1:
            face_value = st.number_input("Face Value (R)", value=1000)
            coupon_rate = st.number_input("Coupon Rate (%)", value=0.05)
            
        with col2:
            maturity = st.number_input("Maturity (years)", value=10)
            frequency = st.number_input("Frequency", value=1)
        
        bond = Bond(face_value, coupon_rate, maturity, frequency)

    with st.container(border=True):
        st.subheader("Yield Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):        
                yield_rate = st.slider("Select a yield rate", min_value=0.0, max_value=1.0, value=0.05, key="analysis_yield")
                bond_price = bond.price(yield_rate)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""
                <style>
                    [data-testid="stMetricValue"] {
                        color: #69F0AE;
                        font-weight: bold;
                    }
                </style>
                """, unsafe_allow_html=True)
                st.metric(label="Bond Price", value=f"R {bond_price:.2f}")


        with col2:
            with st.container(border=True):
                max_market_price = bond.price(0.0001)
                min_market_price = bond.price(1.0)
                market_price = st.slider("Select the bond's market price", min_value=min_market_price, max_value=max_market_price, value=float(face_value), step=1.0, key="analysis_price")
                
                yield_to_maturity = bond.ytm(market_price)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""
                <style>
                    [data-testid="stMetricValue"] {
                        color: #69F0AE;
                        font-weight: bold;
                    }
                </style>    
                """, unsafe_allow_html=True)
                st.metric(label="Yield to Maturity", value=f"{yield_to_maturity:.2f} %")
    
    with st.container(border=True):
        st.subheader("Risk Measures")
        
        yield_rate = st.slider("Select a yield rate", min_value=0.0, max_value=1.0, value=0.05, key="risk_measures_yield")
        macaulay_duration = bond.macaulay_duration(yield_rate)
        modified_duration = bond.modified_duration(yield_rate)
        convexity = bond.convexity(yield_rate)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):        
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""
                <style>
                    [data-testid="stMetricValue"] {
                        color: #69F0AE;
                        font-weight: bold;
                    }
                </style>
                """, unsafe_allow_html=True)
                st.metric(label="Macaulay Duration", value=f"{macaulay_duration:.2f} years")


        with col2:
            with st.container(border=True):        
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""
                <style>
                    [data-testid="stMetricValue"] {
                        color: #69F0AE;
                        font-weight: bold;
                    }
                </style>
                """, unsafe_allow_html=True)
                st.metric(label="Modified Duration", value=f"{modified_duration:.2f} %")

        with col3:
            with st.container(border=True):        
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""
                <style>
                    [data-testid="stMetricValue"] {
                        color: #69F0AE;
                        font-weight: bold;
                    }
                </style>
                """, unsafe_allow_html=True)
                st.metric(label="Convexity", value=f"{convexity:.2f}")


# Relationship Visualization Tab
with tab2:
    with st.container(border=True):
        st.subheader("Visualiser")

        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                st.subheader("Bond 1")    
                face_value_1 = st.number_input("Face Value (R)", value=1000, key="vis_bond_1_fc")
                coupon_rate_1 = st.number_input("Coupon Rate (%)", value=0.05, key="vis_bond_1_cr")
                maturity_1 = st.number_input("Maturity (years)", value=10, key="vis_bond_1_mat")
                frequency_1 = st.number_input("Frequency", value=1, key="vis_bond_1_frq")
                bond_1_enabled = st.checkbox("Enable", value=True, key="bond_1_checkbox")

        with col2:
            with st.container(border=True):
                st.subheader("Bond 2") 
                face_value_2 = st.number_input("Face Value (R)", value=1000, key="vis_bond_2_fc")
                coupon_rate_2 = st.number_input("Coupon Rate (%)", value=0.05, key="vis_bond_2_cr")
                maturity_2 = st.number_input("Maturity (years)", value=10, key="vis_bond_2_mat")
                frequency_2 = st.number_input("Frequency", value=1, key="vis_bond_2_frq")
                bond_2_enabled = st.checkbox("Enable", value=True, key="bond_2_checkbox")

        with col3:
            with st.container(border=True):
                st.subheader("Bond 3") 
                face_value_3 = st.number_input("Face Value (R)", value=1000, key="vis_bond_3_fc")
                coupon_rate_3 = st.number_input("Coupon Rate (%)", value=0.05, key="vis_bond_3_cr")
                maturity_3 = st.number_input("Maturity (years)", value=10, key="vis_bond_3_mat")
                frequency_3 = st.number_input("Frequency", value=1, key="vis_bond_3_frq")
                bond_3_enabled = st.checkbox("Enable", value=True, key="bond_3_checkbox")
            
            bond_1 = Bond(face_value_1, coupon_rate_1, maturity_1, frequency_1)
            bond_2 = Bond(face_value_2, coupon_rate_2, maturity_2, frequency_2)
            bond_3 = Bond(face_value_3, coupon_rate_3, maturity_3, frequency_3)
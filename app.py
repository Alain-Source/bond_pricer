import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from bond import Bond

# Setup & Store App State
# Load startup values
if "bond_defaults" not in st.session_state:
    st.session_state.bond_defaults = {
        "Bond 1": {"fv": 1000, "cr": 0.05, "m": 10, "f": 1},
        "Bond 2": {"fv": 1100, "cr": 0.05, "m": 12, "f": 1},
        "Bond 3": {"fv": 1200, "cr": 0.05, "m": 14, "f": 1},
    }

def save_bond(bond_name):
    st.session_state.bond_defaults[bond_name] = {
        "fv": st.session_state[f"fv_{bond_name}"],
        "cr": st.session_state[f"ni_{bond_name}"],
        "m": st.session_state[f"mat_{bond_name}"],
        "f": st.session_state[f"feq_{bond_name}"],
    }

# Global metric widget stylng using markdown css injection - Green Bold Text
st.markdown("""
     <style>
    [data-testid="stMetricValue"] {
        color: #69F0AE;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Display metric components with standard styling
def display_metric(label, value, prefix="", suffix=""):
    st.markdown("<br>", unsafe_allow_html=True)
    st.metric(label=label, value=f"{prefix}{value:.2f}{suffix}")


# App Title & Sub-title
st.title("Bond Price Calculator")
st.markdown("""An interactive learning tool for exploring fixed-income fundamentals.
<br>Calculate bond prices, yields, and risk measures. 
Visualise bond prices responding to changes in yield rates.""", unsafe_allow_html=True)

# Setup Tabs
tab_Calculator, tab_Visualiser = st.tabs(["Calculator", "Visualiser"])

# Calculator Tab
with tab_Calculator:
    with st.container(border=True):
        st.subheader("Bond Contract")
        
        # Bond Contract section - split the four input fields across two columns (left / right)
        col_contract_left, col_contract_right = st.columns(2)
        with col_contract_left:
            face_value = st.number_input("Face Value (R)", value=1000)
            coupon_rate = st.number_input("Coupon Rate (%)", value=0.05)
            
        with col_contract_right:
            maturity = st.number_input("Maturity (years)", value=10)
            frequency = st.number_input("Frequency", value=1)
        
        # Create an instance / onject of the Bond Class - contains business logic 
        bond = Bond(face_value, coupon_rate, maturity, frequency)

    # Yield Anslysis section - Calculate Bond Price based on provided yield & yield to maturity based on market price
    with st.container(border=True):
        st.subheader("Yield Analysis")
        col_price_calc, col_ytm = st.columns(2)
        
        # Block - Calculate Bond Price based on provided yield
        with col_price_calc:
            with st.container(border=True):        
                yield_rate = st.slider("Select a yield rate", min_value=0.0, max_value=1.0, value=0.05, key="analysis_yield")
                bond_price = bond.price(yield_rate)

                st.markdown("<br>", unsafe_allow_html=True)
                st.metric(label="Bond Price", value=f"R {bond_price:.2f}")

        # Block - Calculate yield to maturity based on market price
        with col_ytm:
            with st.container(border=True):
                max_market_price = bond.price(0.0001)   # Create market price within Bond's ytm methods bisection solver's bounds
                min_market_price = bond.price(1.0)
                market_price = st.slider(
                    "Select the bond's market price", 
                    min_value=min_market_price, 
                    max_value=max_market_price, 
                    value=float(face_value), 
                    step=1.0, key="analysis_price"
                )
                yield_to_maturity = bond.ytm(market_price)
                display_metric("Yield to Maturity", yield_to_maturity, suffix = " %")
    
    # Risk Measures section - display duration & convexity of Bond
    with st.container(border=True):
        st.subheader("Risk Measures")

        # Interactive input slider for User to select yield rate
        yield_rate = st.slider("Select a yield rate", min_value=0.0, max_value=1.0, value=0.05, key="risk_measures_yield")
        
        # Call Bond Class methods to calulcate risk measures
        macaulay_duration = bond.macaulay_duration(yield_rate)
        modified_duration = bond.modified_duration(yield_rate)
        convexity = bond.convexity(yield_rate)
        
        # Display 3 columns for each of the 3 risk measures and display each one next to each other
        col_macaulay_duration, col_modified_duration, col_convexity = st.columns(3)

        # Block - display Macaulay Duration block
        with col_macaulay_duration:
            with st.container(border=True):        
                display_metric("Macaulay Duration", macaulay_duration, suffix = " years")

        # Block - display Modified Duration block
        with col_modified_duration:
            with st.container(border=True):        
                display_metric("Modified Duration", modified_duration, suffix = " %")

        # Block - display Convexity block
        with col_convexity:
            with st.container(border=True):        
                display_metric("Convexity", convexity)


# Price vs Yield Relationship Visualization Tab
with tab_Visualiser:
    with st.container(border=True):
        st.subheader("Visualiser")

        # Create three "pills" / buttons that can be selected as different bond comparison options
        selection = st.pills("Compare bonds", ["Bond 1", "Bond 2", "Bond 3"], selection_mode="multi")
        selection = sorted(selection)   # Sort the three Bonds into the correct order so that Bond 1 always displays to the left of Bond 2, etc.

        # Dynamically build the 3 bond input forms / One, two or three bonds could exist at any point
        bonds = []
        if selection:
            cols = st.columns(len(selection))
            for i, bond_name in enumerate(selection):
                with cols[i]:  
                    with st.container(border=True):
                        st.subheader(bond_name)    
                        defaults = st.session_state.bond_defaults[bond_name]    # Load defaults defined at top of file - startup values

                        # On any event where the input widget is changed, save the new input by calling the save_bond function 
                        # Pass in a unique key for each Bond's widgets as an ID for Streamlit to be able to identify
                        fv = st.number_input("Face Value (R)", value=defaults["fv"], key=f"fv_{bond_name}", on_change=save_bond, args=(bond_name,))     
                        cr = st.number_input("Coupon Rate (%)", value=defaults["cr"], key=f"ni_{bond_name}", on_change=save_bond, args=(bond_name,))
                        m = st.number_input("Maturity (years)", value=defaults["m"], key=f"mat_{bond_name}", on_change=save_bond, args=(bond_name,))
                        f = st.number_input("Frequency", value=defaults["f"], key=f"feq_{bond_name}", on_change=save_bond, args=(bond_name,))
                        
                bonds.append(Bond(fv, cr, m, f))    # Use input data from relevant Bond to create an instance of the Bond class for Bond 1, 2, 3.

            # Build the Comparison Graph
            # Build using the pyplot module from the Matplotlib package
            yield_range = np.linspace(0.01, 0.15, 100)      # Define a range of yield rates over which the bonds can be compared
            fig, ax = plt.subplots()    
            for i, bond_name in enumerate(selection):
                ax.plot(yield_range * 100, bonds[i].price_range(yield_range), label=bond_name)  # Add a new graph as a subplot onto the same figure
            ax.set_title("Price-Yield Comparison")
            ax.set_xlabel("Yield [%]")
            ax.set_ylabel("Bond Price [R]")
            ax.legend()
            st.pyplot(fig)  # Call to Streamlit to display the Matplotlib pyplot figure
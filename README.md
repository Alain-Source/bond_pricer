# Bond Price Calculator
An interactive learning tool for exploring fixed-income fundamentals.

## Overview
A basic calculator to price fixed-rate bonds.
Project uses a Streamlit app for visualisation and is intended to be used as a learning project.
Calculate bond prices, yields, macaulay duration, modified duration and the convexity of a bond.
Compare up to three bonds to visualise and compare bond prices for different yield rates.

![Bond Calculator](images/Bond Calculator.png)

![Bond Visualiser](images/Bond Visualiser.png)


## How to Run
```bash
git clone https://github.com/Alain-Source/bond_pricer.git
cd bond_pricer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Command Line**
```bash
python3 main.py
```

**Interactive Web App**
```bash
streamlit run app.py
```

**Run Tests**
```bash
python3 test_bond.py
```

## Financial Theory

Present Value

Bond Pricing

Yield-to-maturity

Macaulay duration

Modified duration

Convexity


## Project Structure

```
bond_pricer/
├── bond.py          Bond class — pricing, YTM, duration, convexity
├── main.py          CLI testing script
├── app.py           Streamlit interactive web app & primary means of using the calculator
├── test_bond.py     Unit tests for Bond class
├── requirements.txt Python dependencies
└── README.md        Project documentation
```

## Testing


## What I Learned & Next Steps
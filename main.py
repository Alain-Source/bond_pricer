from re import S
from bond import Bond
import numpy as np
import matplotlib.pyplot as plt

def main():  # Main function not required in Python (like in C). Used for organization as codebase grows

    # Testing Bond methods
    test_bond = Bond(face_value=1000,coupon_rate=0.05, maturity=10, frequency=1)
    print("BOND 1")
    print(f"Price:              {test_bond.price(0.05)}")
    print(f"YTM:                {test_bond.ytm(1000)}")
    print(f"Macaulay Duration:  {test_bond.macaulay_duration(0.05)}")
    print(f"Modified Duration:  {test_bond.modified_duration(0.05)}")
    print(f"Convexity:          {test_bond.convexity(0.05)}")

    # Testing Bond methods
    test_bond_2 = Bond(face_value=1000, coupon_rate=0.05, maturity=10, frequency=1)
    print("\nBOND 2")
    print(f"Price:              {test_bond_2.price(0.05)}")
    print(f"Macaulay Duration:  {test_bond_2.macaulay_duration(0.05)}")
    print(f"Modified Duration:  {test_bond_2.modified_duration(0.05)}")
    print(f"Convexity:          {test_bond_2.convexity(0.05)}")
    
    # Investigate the relationship between yeild rates & bond prices
    yield_range = np.linspace(0.01, 0.15, 100)
    yield_range_prices = []
    for i in range(len(yield_range)):
        yield_range_prices.append(test_bond.price(yield_range[i]))
    
    # Plot the relationship between yeild rates & bond prices. 
    # Save it to price_yield_curve.png
    plt.plot(yield_range, yield_range_prices)
    plt.title("Yield vs Price Relationship")
    plt.xlabel("Yield")
    plt.ylabel("Bond Prices")
    plt.tight_layout()
    plt.savefig("price_yield_curve.png")
    plt.clf()

    # Multiple Maturity Bond Comparison
    short_bond = Bond(face_value=1000,coupon_rate=0.02, maturity=2, frequency=1)       # Short maturity bond
    medium_bond = Bond(face_value=1000,coupon_rate=0.05, maturity=10, frequency=1)      # Medium maturity bond
    long_bond = Bond(face_value=1000,coupon_rate=0.08, maturity=30, frequency=1)        # Long maturity bond

    short_bond_prices = short_bond.price_range(yield_range)
    medium_bond_prices = medium_bond.price_range(yield_range)
    long_bond_prices = long_bond.price_range(yield_range)

    # Plot the relationship between yeild rates & bond prices. 
    # Save it to price_yield_curve.png
    plt.figure()
    plt.plot(yield_range, short_bond_prices, label="2yr, 2% coupon")
    plt.plot(yield_range, medium_bond_prices, label="10yr, 5% coupon")
    plt.plot(yield_range, long_bond_prices, label="30yr, 8% coupon")
    plt.legend()
    plt.xlabel("Yield")
    plt.ylabel("Bond Prices")
    plt.tight_layout()
    plt.savefig("bond_comparison.png")


if __name__ == "__main__":
    main()
from bond import Bond

def main():  # Main function not required in Python (like in C). Used for organization as codebase grows
    test_bond = Bond(face_value=1000,coupon_rate=0.05, maturity=10, frequency=1)
    print("BOND 1")
    print(f"Price:              {test_bond.price(0.05)}")
    print(f"YTM:                {test_bond.ytm(1000)}")
    print(f"Macaulay Duration:  {test_bond.macaulay_duration(0.05)}")
    print(f"Modified Duration:  {test_bond.modified_duration(0.05)}")
    print(f"Convexity:          {test_bond.convexity(0.05)}")

    test_bond_2 = Bond(face_value=1000, coupon_rate=0.0, maturity=10, frequency=1)
    print("\nBOND 2")
    print(f"Price:              {test_bond_2.price(0.05)}")
    print(f"Macaulay Duration:  {test_bond_2.macaulay_duration(0.05)}")
    print(f"Modified Duration:  {test_bond_2.modified_duration(0.05)}")
    print(f"Convexity:          {test_bond_2.convexity(0.05)}")

if __name__ == "__main__":
    main()
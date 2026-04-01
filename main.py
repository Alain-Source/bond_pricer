from bond import Bond

def main():  # Main function not required in Python like in languages like C. Used for organization as codebase grows
    test_bond = Bond(face_value=1000,coupon_rate=0.05, maturity=10, frequency=1)
    print(test_bond.price(0.05))

if __name__ == "__main__":
    main()
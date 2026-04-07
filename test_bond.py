import unittest
from bond import Bond

class TestBond(unittest.TestCase):
    """Unit tests for BOnd Class Input Handling, Bond Pricing, Yield, and Risk Measure calculations."""

    # Input Handling
    def test_negative_input_causes_error(self):
        with self.assertRaises(ValueError):
            Bond(-1000, 0.05, 10, 1)
    
    def test_frequency_not_option_causes_error(self):
        with self.assertRaises(ValueError):
            Bond(1000, 0.05, 10, 3)

    def test_negative_coupon_rate_causes_error(self):
        with self.assertRaises(ValueError):
            Bond(1000, -0.05, 10, 1)

    def test_coupon_rate_above_one_causes_error(self):
        with self.assertRaises(ValueError):
            Bond(1000, 1.1, 10, 1)

    def test_negative_maturity_causes_error(self):
        with self.assertRaises(ValueError):
            Bond(1000, 0.05, -10, 1)

    def test_zero_maturity_causes_error(self):
        with self.assertRaises(ValueError):
            Bond(1000, 0.05, 0, 1)

    def test_float_maturity_causes_error(self):
        with self.assertRaises(ValueError):
            Bond(1000, 0.05, 10.3, 1)

    # Calculation Validation
    def test_par_bond_price(self):
        bond = Bond(1000, 0.05, 10, 1)
        self.assertAlmostEqual(bond.price(0.05), 1000, places = 2)

    def test_semi_annual_par_bond_price(self):
        bond = Bond(1000, 0.05, 10, 2)
        self.assertAlmostEqual(bond.price(0.05), 1000, places = 2)

    def test_zero_coupon_duration_equals_maturity(self):
        bond = Bond(1000, 0.0, 30, 1)
        self.assertAlmostEqual(bond.macaulay_duration(0.05), 30, places=2)

    def test_modified_duration(self):
        bond = Bond(1000, 0.05, 10, 1)
        self.assertAlmostEqual(bond.modified_duration(0.05), 7.7217, places=2)
        
    def test_ytm_price(self):
        bond = Bond(1000, 0.05, 10, 1)
        self.assertAlmostEqual(bond.ytm(565.90), 0.13, places=2)

    def test_convexity_always_positive(self):
        bond = Bond(1000, 0.05, 10, 1)
        self.assertGreater(bond.convexity(0.05), 0)

    def test_long_bond_has_higher_convexity(self):
        long_bond = Bond(1000, 0.05, 20, 1)
        short_bond = Bond(1000, 0.05, 5, 1)
        self.assertGreater(long_bond.convexity(0.05), short_bond.convexity(0.05))

    def test_modified_duration_less_than_macaulay(self):
        bond = Bond(1000, 0.05, 10, 1)
        self.assertLess(bond.modified_duration(0.05), bond.macaulay_duration(0.05))

if __name__ == "__main__":
    unittest.main()

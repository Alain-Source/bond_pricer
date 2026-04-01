class Bond:

    def __init__(self, face_value, coupon_rate, maturity, frequency) -> None:   # initialise the c
        self.face_value = face_value
        self.coupon_rate = coupon_rate      # Percentage of face value which determines the coupon payment
        self.maturity = maturity            # Number of years to bond maturity
        self.frequency = frequency          # Number of bond payments per year

    def price(self, yield_rate):        
        # Face value multiplied by coupon rate for total yearly coupon payment. 
        # Frequency adjusts payment to account for number of payments in a year
        coupon_payment = self.face_value * self.coupon_rate / self.frequency

        # Maturity is the number of years to bond maturity.
        # Frequency adjusts for number of payments per year.
        total_num_payments = self.maturity * self.frequency 

        # Yield per coupon payment
        period_yield_rate = yield_rate / self.frequency  
                                                                               
        bond_price = 0                                                                                    # Bond Price Formula | PV = SUM_1_to_n(PMT / (1 + r)^n) + FV/(1 + r)^n , n = {1,2,..,n} 
        for i in range(1, total_num_payments):                                                            # Range from 1 to n-1 as the final payment will include interest payment & face value.
            bond_price += coupon_payment/(1 + period_yield_rate) ** i                                     # Coupon payment per period (i) added to the total coupon payment
        bond_price += (coupon_payment + self.face_value)/(1 + period_yield_rate) ** total_num_payments    # Final payment includes coupon payment & face value
        return bond_price

    def ytm(self, market_price, accuracy = 0.0001):    # implement a bescetion guess method
        test_yield_lower_bound = 0.0001
        test_yield_upper_bound = 1
        
        midpoint = (test_yield_upper_bound + test_yield_lower_bound) / 2    # Guess what the yield is by testing the midpoint between the two values
        test_price = self.price(midpoint)                                   # Calculate what the bond price is at that midpoint yield

        # Check whether the price resulting from the test yield's bounds equal to 
        # or within the specified accuracy of the market price.
        while abs(test_price - market_price) >= accuracy:                       
            if market_price > test_price:                                       
               test_yield_upper_bound = midpoint                                # test_price is less than the market price (the upper bound was too high)
            else:
                test_yield_lower_bound = midpoint                               # test_price is greater than the market price (the lower bound was too low)
            
            midpoint = (test_yield_upper_bound + test_yield_lower_bound) / 2    # Guess what the yield is by testing the midpoint between the two values
            test_price = self.price(midpoint)                                   # Calculate what the bond price is at that midpoint yeild

        return midpoint
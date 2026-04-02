class Bond:

    def __init__(self, face_value, coupon_rate, maturity, frequency) -> None:   # initialise the class
        self.face_value = face_value
        self.coupon_rate = coupon_rate      # Percentage of face value which determines the coupon payment
        self.maturity = maturity            # Number of years to bond maturity
        self.frequency = frequency          # Number of bond payments per year

        # Compute coupon_payment & total_num_payments once at object initialization

        # Face value multiplied by coupon rate for total yearly coupon payment. 
        # Frequency adjusts payment to account for number of payments in a year
        self.coupon_payment = self.face_value * self.coupon_rate / self.frequency   
        # Frequency adjusts for number of payments per year.
        self.total_num_payments =  self.maturity * self.frequency                   

    def _present_value(self, cash_flow, period_yield_rate, period):          # Internal class helper method
        return cash_flow/(1 + period_yield_rate) ** period                   # Per period present_value calculation

    
    def price(self, yield_rate):        
        # Yield per coupon payment
        period_yield_rate = yield_rate / self.frequency  
                                                                               
        bond_price = 0                                                                                                         # Bond Price Formula | PV = SUM_1_to_n(PMT / (1 + r)^n) + FV/(1 + r)^n , n = {1,2,..,n} 
        for i in range(1, self.total_num_payments):                                                                            # Range from 1 to n-1 as the final payment will include interest payment & face value.
            bond_price += self._present_value(self.coupon_payment, period_yield_rate, i)                                       # Coupon payment per period (i) added to the total coupon payment
        bond_price += self._present_value(self.coupon_payment + self.face_value, period_yield_rate, self.total_num_payments)   # Final payment includes coupon payment & face value
        return bond_price

    def ytm(self, market_price, accuracy = 0.0001):                             # implement bisection guess method
        test_yield_lower_bound = 0.0001
        test_yield_upper_bound = 1
        
        midpoint = (test_yield_upper_bound + test_yield_lower_bound) / 2        # Guess what the yield is by testing the midpoint between the two values
        test_price = self.price(midpoint)                                       # Calculate what the bond price is at that midpoint yield

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

    # Macaulay Duration is the weighted average time to receive the bond's cash flows.
    # Macaulay duration is a linear approximation of price changes based on yield changes.
    def macaulay_duration(self, yield_rate):   
        period_yield_rate = yield_rate / self.frequency  
                                                                               
        weighted_present_value = 0                                                                                            # Weight each period's payment by it's payment number                                                                    
        for i in range(1, self.total_num_payments):                                                            
            weighted_present_value += self._present_value(self.coupon_payment, period_yield_rate, i) * i / self.frequency     # Weight by (period / frequency of payments per period) to determine payment number                      
        weighted_present_value += self._present_value(self.coupon_payment + self.face_value, period_yield_rate, self.total_num_payments) * self.total_num_payments/ self.frequency 
        return weighted_present_value / self.price(yield_rate)

    # Modified macaulay duration provides the approximate percentage price change for a 1% change in yield."
    def modified_duration(self, yield_rate):          
        return self.macaulay_duration(yield_rate) / (1 + yield_rate / self.frequency)

    # Convexity measures the curvature of the price-yield relationship.
    # Convexity better describes the curved price-yield relationship compared to Macaulay's linear approximation
    def convexity(self, yield_rate):
        period_yield_rate = yield_rate / self.frequency  
                                                                               
        weighted_present_value = 0                                                                                                                                                               
        for i in range(1, self.total_num_payments):                                                            
            weighted_present_value += self._present_value(self.coupon_payment, period_yield_rate, i) * i * (i + 1)                         
        weighted_present_value += self._present_value(self.coupon_payment + self.face_value, period_yield_rate, self.total_num_payments) * self.total_num_payments * (self.total_num_payments + 1) 
        weighted_present_value / (self.price(yield_rate) * (1 + period_yield_rate) ** 2 * self.frequency ** 2)
        return weighted_present_value
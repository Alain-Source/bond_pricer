class Bond:

    def __init__(self, face_value, coupon_rate, maturity, frequency):
        """Initialise fixed-rate bond object instance for the class.
    
        Args:
            face_value: Principal paid at bond's maturity (e.g. 1000)
            coupon_rate: Annual coupon as a decimal representing percentage of face value (e.g. 0.05 for 5%)
            maturity: Number of years to maturity
            frequency: Coupon payments per year (1 = annual, 2 = semi-annual)
        """
        if face_value <= 0:
            raise ValueError("Face value must be positive")
        if not 0 <= coupon_rate <= 1:
            raise ValueError("Coupon rate must be between 0 and 1")
        if maturity <= 0:
            raise ValueError("Maturity must be positive")
        if not isinstance(maturity, int):
            raise ValueError("Maturity must be a whole number to represent years")
        if frequency not in [1, 2, 4, 12]:
            raise ValueError("Frequency must be 1 (annual), 2 (semi-annual), 4 (quarterly), or 12 (monthly)")

        self.face_value = face_value
        self.coupon_rate = coupon_rate      
        self.maturity = maturity           
        self.frequency = frequency          

        # Coupon payment per period. 
        self.coupon_payment = self.face_value * self.coupon_rate / self.frequency   
        self.total_num_payments = self.maturity * self.frequency                   

    def _present_value(self, cash_flow, period_yield_rate, period): 
        """Discount a single cash flow to its present value.
    
        Args:
            cash_flow: The payment amount to discount.
            period_yield_rate: Yield per period as a decimal.
            period: Number of periods to discount over.
        
        Returns:
            Present value of the cash flow.
        """
        return cash_flow/(1 + period_yield_rate) ** period                   

    
    def price(self, yield_rate):        
        """Calculate the bond price based on a provided yield_rate
           
        Args:
            yield_rate: Annual yield as a decimal (e.g. 0.05 for 5%)
        
        Returns:
            Bond price as a float (e.g. 12532.45)
        """
        if yield_rate < 0:
            raise ValueError("Yield rate cannot be negative")

        period_yield_rate = yield_rate / self.frequency  
                                                                               
        bond_price = 0                                                                                                         # Bond Price Formula | PV = SUM_1_to_n(PMT / (1 + r)^n) + FV/(1 + r)^n , n = {1,2,..,n} 
        for i in range(1, self.total_num_payments):                                                                            # Range from 1 to n-1 as the final payment will include interest payment & face value.
            bond_price += self._present_value(self.coupon_payment, period_yield_rate, i)                                       # Coupon payment per period (i) added to the total coupon payment
        bond_price += self._present_value(self.coupon_payment + self.face_value, period_yield_rate, self.total_num_payments)   # Final payment includes coupon payment & face value
        return bond_price

    def ytm(self, market_price, accuracy = 0.0001):                             
        """Calculate the yield to maturity based on a bond's market price
           Implements a bisection method to determine yield
           
        Args:
            market_price: Bond's price set by market (e.g. 12523.26)
            accuracy: Describes how close the bisection method's resulting midpoint yield's price should be to the market_price

        Returns:
            Yield to maturity as a decimal (e.g. 0.05 for 5%)
        """
        if market_price <= 0:
            raise ValueError("Market price must be positive")

        test_yield_lower_bound = 0.0001
        test_yield_upper_bound = 1
        midpoint = (test_yield_upper_bound + test_yield_lower_bound) / 2        # Guess what the yield is by testing the midpoint between the two values
        test_price = self.price(midpoint)                                       # Calculate what the bond price is at that midpoint yield
        iterations = 0
    
        # Check whether the price resulting from the test yield's bounds equal to 
        # or within the specified accuracy of the market price.
        while abs(test_price - market_price) >= accuracy:                       
            if iterations > 1000:
                raise ValueError("YTM did not converge — market price outside valid range")
            if market_price > test_price:                                       
               test_yield_upper_bound = midpoint                                # test_price is less than the market price (the upper bound was too high)
            else:
                test_yield_lower_bound = midpoint                               # test_price is greater than the market price (the lower bound was too low)
            
            midpoint = (test_yield_upper_bound + test_yield_lower_bound) / 2    # Guess what the yield is by testing the midpoint between the two values
            test_price = self.price(midpoint)   
            iterations += 1                                # Calculate what the bond price is at that midpoint yield
        return midpoint


    def macaulay_duration(self, yield_rate):   
        """Calculate the weighted average time to receive the bond's cash flows.
        Provides a linear approximation of price sensitivity to yield changes.
            
        Args:
            yield_rate: Annual yield as a decimal (e.g. 0.05 for 5%)
        
        Returns:
            Duration in years.
        """
        period_yield_rate = yield_rate / self.frequency  
                                                                               
        weighted_present_value = 0                                                                                            # Weight each period's payment by its payment number                                                                    
        for i in range(1, self.total_num_payments):                                                            
            weighted_present_value += self._present_value(self.coupon_payment, period_yield_rate, i) * i / self.frequency     # Weight by (period / frequency of payments per period) to determine payment number                      
        weighted_present_value += self._present_value(self.coupon_payment + self.face_value, period_yield_rate, self.total_num_payments) * self.total_num_payments/ self.frequency 
        return weighted_present_value / self.price(yield_rate)


    def modified_duration(self, yield_rate): 
        """Calculate the approximate percentage price change for a 1% change in the yield rate.
            
        Args:
            yield_rate: Annual yield as a decimal (e.g. 0.05 for 5%)
        
        Returns:
            Percentage price change as a decimal (e.g. 0.0762 for 7.62%)
        """
        return self.macaulay_duration(yield_rate) / (1 + yield_rate / self.frequency)


    def convexity(self, yield_rate):
        """Calculate the convexity of the bond
        Convexity measures the curvature of the price-yield relationship.
            
        Args:
            yield_rate: Annual yield as a decimal (e.g. 0.05 for 5%)
        
        Returns:
            Convexity as a float (e.g. 12542.23556)
        """
        period_yield_rate = yield_rate / self.frequency  
                                                                               
        weighted_present_value = 0                                                                                                                                                                                                                   
        for i in range(1, self.total_num_payments):                                                            
            weighted_present_value += self._present_value(self.coupon_payment, period_yield_rate, i) * i * (i + 1)          # Convexity weights present value by i * (i + 1)                  
        weighted_present_value += self._present_value(self.coupon_payment + self.face_value, period_yield_rate, self.total_num_payments) * self.total_num_payments * (self.total_num_payments + 1) 
        return weighted_present_value / (self.price(yield_rate) * (1 + period_yield_rate) ** 2 * self.frequency ** 2)


    def price_range(self, yield_range):
        """Calculate the Bond's price for a list of provided yield values
            
        Args:
            yield_range: List of annual yields as decimals
        
        Returns:
            List of Bond Prices
        """
        return [self.price(y) for y in yield_range]
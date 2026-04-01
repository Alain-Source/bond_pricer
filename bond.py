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
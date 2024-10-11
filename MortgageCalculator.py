#@author Omar Abou

import pandas as pd  # This lets us work with data in a table-like format

class MortgageCalculator:
    # This sets up the calculator with all the information about the mortgage
    def __init__(self, amount_borrowed, years, annual_interest, annual_property_tax, annual_property_insurance, annual_pmi_rate):
        self.amount = float(amount_borrowed)
        self.years = int(years)
        self.annual_interest = float(annual_interest)
        self.annual_property_tax = float(annual_property_tax)
        self.annual_property_insurance = float(annual_property_insurance)
        self.annual_pmi_rate = float(annual_pmi_rate)
        self.monthly_interest = (self.annual_interest / 100) / 12
        self.loan_term = self.years * 12

    # This calculates the total monthly payment
    def get_monthly_payment(self):
        if self.monthly_interest == 0:
            monthly_payment = self.amount / self.loan_term
        else:
            # This is the formula for calculating the monthly mortgage payment
            monthly_payment = (self.monthly_interest * self.amount * (1 + self.monthly_interest) ** self.loan_term) / ((1 + self.monthly_interest) ** self.loan_term - 1)

        # Add other monthly costs
        monthly_payment += self.annual_property_tax / 12
        monthly_payment += self.annual_property_insurance / 12
        monthly_payment += (self.annual_pmi_rate / 100 * self.amount) / 12

        return monthly_payment

    # This creates a detailed breakdown of each payment over the life of the loan
    def generate_amortization_table(self):
        monthly_payment = self.get_monthly_payment()
        balance = self.amount
        amortization_table = []

        for month in range(1, self.loan_term + 1):
            interest_payment = balance * self.monthly_interest
            principal_payment = monthly_payment - interest_payment - (self.annual_property_tax / 12) - (self.annual_property_insurance / 12) - ((self.annual_pmi_rate / 100 * self.amount) / 12)
            balance -= principal_payment

            # Add this month's payment information to the table
            amortization_table.append({
                'Month': month,
                'Payment': monthly_payment,
                'Principal': principal_payment,
                'Interest': interest_payment,
                'Property Tax': self.annual_property_tax / 12,
                'Property Insurance': self.annual_property_insurance / 12,
                'PMI': (self.annual_pmi_rate / 100 * self.amount) / 12,
                'Balance': max(0, balance)  # Make sure the balance doesn't go below zero
            })

        return pd.DataFrame(amortization_table)

    # This calculates the total interest paid over the life of the loan
    def total_interest_paid(self):
        amortization_table = self.generate_amortization_table()
        return amortization_table['Interest'].sum()

    # This calculates the total amount paid over the life of the loan
    def total_cost(self):
        amortization_table = self.generate_amortization_table()
        return amortization_table['Payment'].sum()
    
# This function makes sure the user enters a valid number
def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

# This part gets information from the user
print("\n")
print("Welcome to the Mortgage Calculator Demo Project")
print("\n")
amount = get_float_input("Enter the amount borrowed: ")
years = get_float_input("Enter the number of years to pay back: ")
annual_interest = get_float_input("Enter the annual interest rate (%): ")
annual_property_tax = get_float_input("Enter the annual property tax: ")
annual_property_insurance = get_float_input("Enter the annual property insurance cost: ")
annual_pmi_rate = get_float_input("Enter the annual private mortgage insurance rate (%): ")

# This function prints out the payment breakdown table
def print_amortization_table(table, num_rows= int(years * 12)):
    print("\nAmortization Table:")
    print(table.head(num_rows).to_string(index=False, float_format='${:,.2f}'.format))
    print("\n...\n")
    print(table.tail(1).to_string(index=False, float_format='${:,.2f}'.format))

# Create a new mortgage calculator with the user's information
calculator = MortgageCalculator(amount, years, annual_interest, annual_property_tax, annual_property_insurance, annual_pmi_rate)

# Calculate and show the results
monthly_payment = calculator.get_monthly_payment()
total_interest = calculator.total_interest_paid()
total_cost = calculator.total_cost()

print(f"\nYour monthly payment is: ${monthly_payment:.2f}")
print(f"Your total interest paid over the life of the loan is: ${total_interest:.2f}")
print(f"Your total cost over the life of the loan is: ${total_cost:.2f}")

# Create and show the payment breakdown table
amortization_table = calculator.generate_amortization_table()
print_amortization_table(amortization_table)
print("\n") # Extra space
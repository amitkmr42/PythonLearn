# Tip Calculator (Floats & Rounding): Prompt the user for a restaurant bill amount (as a float). 
# Calculate a 15% tip, and use the round() function to display the final total rounded to two decimal places.

def main():
    bill=float(input("Enter the restaurant bill amount: "))
    tip= bill*0.15
    tbill=round(bill+tip,2)
    print("Your total bill is:", tbill)

main()

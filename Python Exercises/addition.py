# Type Conversion Calculator: Ask the user for two integers using input(). 
# Convert them from strings to integers, add them together, and print the total.

def main():
    x=input("Enter first number: ")
    y=input("Enter second number: ")
    z= int(x)+int(y)
    print(f"Total is {z}")

main()
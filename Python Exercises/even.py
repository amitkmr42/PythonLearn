# Parity Checker: Write a program that asks the user for a number. 
# Use an if/else statement and the modulo (%) operator to print "Even" 
# if the number is divisible by 2, and "Odd" otherwise.

def main():
    x=int(input("What is x? "))
    if x%2 == 0:
        print("Even")
    else: 
        print("Odd")

main()
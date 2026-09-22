# Returning Values: Write a square(n) function that mathematically squares a number and uses the return keyword. 
# In your main code, ask the user for a number, pass it to square(), and print the returned value.

def square (n):
    return n*n

def main():
    x=int(input("Enter a number to be sqaured: "))
    print(f"The square of the number {x} is {square(x)}")

main()
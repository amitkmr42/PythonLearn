# Boolean Returns: Define a function is_positive(n) that returns the boolean True 
# if n is greater than zero, and False otherwise. Take a user's input, pass it to the function, 
# and print the resulting boolean.

def main():
    x= int(input("Enter a number: "))
    print("Is the number positive?", check(x))

def check(n):
    if n>=0:
        return True
    else:
        return False

main()
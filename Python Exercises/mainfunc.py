# The main Structure: Define a main() function and a separate greet(name) function. 
# Have your program start by calling main(), which prompts the user for their name 
# and then passes it to greet() to be printed.

def main():
    name=input("Enter you name: ")
    greet(name)

def greet(name):
    print("Hi,",name)

main()

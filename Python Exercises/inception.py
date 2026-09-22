# Quote Inception: Write a program that asks the user for a quote and the author. 
# Use an f-string to print a sentence containing both single and double quotes. 
# (Example output: The instructor said, "Python's strings are versatile!")

def main():
    quote=input("Enter a quote: ")
    author=input("Enter the author of the quote: ")
    print(f"The {author} said, \"{quote}\"")

main()
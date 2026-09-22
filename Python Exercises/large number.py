# F-String Formatting: Ask the user to input a very large number (like 1000000). 
# Print the number back to them with comma separators using f-string formatting techniques (e.g., f"{number:,}").


def main():
    number=int(input("Enter large number: "))
    print("Large number is ",f"{number:,}")

main()
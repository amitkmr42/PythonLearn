# The Cleanup Crew: Write a program that asks for a user's full name. 
# Chain string methods to strip any extra whitespace from the beginning and end, and 
# convert their input to title case. Print the cleaned-up name.

def main():
    name=input("Enter your full name: ").strip().title()
    print(f"Your name is: {name}")

main()
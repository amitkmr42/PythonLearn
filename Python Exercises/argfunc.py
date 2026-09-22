# Default Parameters: Create a function describe_character(name, role="NPC"). 
# Call the function twice from your main code: once providing both a name and a role, 
# and once providing only the name so it falls back to the default "NPC" role.

def main():
    name = input("Enter your name: ")
    role = input("Enter your role: ")
    describe_character(name, role)
    describe_character(name)

def describe_character(name, role="NPC"):
    print(f"Name: {name}, Role: {role}")

main()
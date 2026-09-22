# Chained Comparisons: Ask the user for their age. Use a chained comparison (e.g., 13 <= age <= 19) 
# in an if statement to evaluate if they are a teenager, printing a corresponding message based on the result.

def main():
    age=input("Enter your age: ")
    if 13 <= int(age) <= 19:
        print("You are a teenager.")
    else:
        print("You are not a teenager.")

main()
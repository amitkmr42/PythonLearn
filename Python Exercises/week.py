# Modulo Math: Ask the user for a random number of days (e.g., 25). 
# Calculate and print how many full weeks and remaining days that equals 
# (e.g., 25 days is 3 weeks and 4 days) using floor division and the modulo % operator.

def main():
    days=int(input("Enter number of days: "))
    week=days//7
    day=days%7
    print(f"{days} days is {week} weeks and {day} days")

main()
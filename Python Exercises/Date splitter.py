# Date Splitter: Prompt the user for a date in the format "MM/DD/YYYY". 
# Use the .split() method to separate the month, day, and year, assigning them to different variables, and 
# print them on separate lines.

def main():
    date=input("Enter a date in MM/DD/YYYY format: ")
    date=date.split("/")
    print(f"Date is {date[1]}")
    print(f"Month is {date[0]}")
    print(f"Year is {date[2]}")


main()
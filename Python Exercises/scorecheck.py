# Grade Calculator: Create a program that takes a test score (0-100) as an integer. 
# Use if, elif, and else to output "A" for 90-100, "B" for 80-89, "C" for 70-79, 
# and "F" for anything below 70.

def main():
    x= int(input("Enter your score between 0-100: "))
    if x>90:
        print("Grade: A")
    elif x>=80:
        print("Grade: B")
    elif x>=70:
        print("Grade: C")
    else:
        print("Grade: F")

main()
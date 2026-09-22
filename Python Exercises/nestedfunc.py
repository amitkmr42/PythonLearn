# Nested Functions: Prompt the user for a floating-point number. 
# In a single line of code (by nesting your functions), convert their input into a rounded integer and print it.

def main():
    num=input("Enter a floating point number: ")
    print(fl(num))

def fl(num):
        num=float(num)
        num=round(num)
        return num

main()
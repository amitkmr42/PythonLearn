# Scope Practice: Write a program to calculate the volume of a cube. 
# Define a function get_volume(side) that returns side * side * side. 
# Make sure you define the side variable locally inside your main function to practice local scope.

def get_vol(x):
    return x*x*x

def main():
    n= int(input("Enter the length of the side of the cube: "))
    print(f"The volume of the cube is: {get_vol(n)}")

main()
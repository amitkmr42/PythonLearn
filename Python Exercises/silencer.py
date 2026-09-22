# Indoor Voice: Ask the user to input a "loud" sentence (all uppercase). 
# Use a string method to convert the entire sentence to lowercase, and print the quieted down sentence.

def main():
    loud=input("Enter a loud noise (in all caps): ").lower()
    print("You have said loudly. It should be silenced and spoken as: ", loud)

main()
# Video Game Controls (match case): Ask the user to input a movement key 
# ("w", "a", "s", or "d"). Use a match statement to print "Up", "Left", "Down", or "Right". 
# Include a catch-all case _: to print "Invalid key" if they type something else.

def main():
    x= input("Enter where you want to move (w, a, s, d): ")
    match x:
        case "w":
            print("Up")
        case "a":
            print("Left")
        case "s":
            print("Down")
        case "d":
            print("Right")
        case default:
            print("Invalid Key")

main()
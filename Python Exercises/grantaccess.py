# Double Verification (AND logic): Ask for a username and a password. 
# Print "Access Granted" only if the username is "admin" and the password is "python123". 
# Otherwise, print "Access Denied".

def main():
    user=input("Enter the username: ")
    passw=input("Enter the password: ")
    if user == "admin" and passw == "python123":
        print ("Access Granted")
    else:
        print ("Access Denied")

main()
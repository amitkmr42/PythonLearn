import re

email = input("What's your email address? ").strip()

if re.search("..*@..*",email):
    print("Valid")
else:
    print("Invalid")
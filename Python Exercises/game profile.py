# Game Profile (F-Strings): Ask the user for their favorite video game and their favorite character. 
# Use a single f-string to print: "Your favorite game is [Game] and you love playing as [Character]!"


def main():
    game=input("Enter your favourite game: ")
    ch=input("Enter your favourite character: ")
    print(f"Your favourite game is {game} and you love playing as {ch}")

main()
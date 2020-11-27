from Table import Table

def main():
    print("Welcome to Michael Harbidge's Poker program.")
    print("The game will now begin setup. This can be repeated later.")
    table = Table()
    inputting = True
    while inputting:
        table.display_players()
        print("To play a round with the current setup, type P.")
        print("To setup the game again, type S.")
        print("To quit, type Q.")
        input_str = input("Input: ")
        if input_str.upper() == "P":
            table.round()
        elif input_str.upper() == "S":
            table = Table()
        elif input_str.upper() == "Q":
            inputting = False
        else:
            print("Invalid Input.")

main()
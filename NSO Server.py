from flask import *

def addMessage():



def getMessage():



def delMessage():



def main():
    option = int(input("What option would you like?\n1. Add a message to the server.\n2. Retrieve a message from the server.\n3. Delete a message from the server.\n"))
    if option == 1:
        addMessage()
    elif option == 2:
        getMessage()
    elif option == 3:
        delMessage()


if __name__ == "__main__":
    main()

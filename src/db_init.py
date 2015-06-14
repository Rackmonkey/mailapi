import getpass
import models
from mailapi import db

def create_default_values():
    rank = models.Rank(1, 'Moderator')
    db.session.add(rank)

    rank = models.Rank(2, 'User')
    db.session.add(rank)
    db.session.commit()

def create_account():
    username = input("Please enter a username for the first Account: ")
    password = getpass.getpass("Please enter a safety password: ")

    admin_account = models.Admin(username, password)
    db.session.add(admin_account)
    db.session.commit()

    return True


if __name__ == "__main__":
    create_default_values()

    if create_account():
        print("Successfully installed mailapi, Happy Mailing :)")
    else:
        print("An error occured")

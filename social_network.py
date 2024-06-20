import json
import re
from user import User

class SocialNetwork:
    def __init__(self):
        self.users = {}
        self.logins = {}
        self.load_users()

    def validate_email(self, login):
        return re.match(r"^[^@]+@(gmail\.com|hotmail\.com)$", login)

    def validate_password(self, password):
        return any(char.isupper() for char in password)

    def create_account(self, user_id, name, login, password):
        if not self.validate_email(login):
            print("❌ Login must be a valid email containing '@'.")
        elif login in self.logins:
            print("❌ Login is already in use.")
        elif user_id in self.users:
            print("❌ User with this ID already exists.")
        else:
            user = User(user_id, name, login, password)
            self.users[user_id] = user
            self.logins[login] = user_id
            self.save_users()
            print("✔️ Account successfully created for {}.".format(name))

    def authenticate(self, login, password):
        if login in self.logins:
            user_id = self.logins[login]
            user = self.users[user_id]
            if user.password == password:
                print("✔️ Authentication successful for {}.".format(user.name))
                return user_id
            else:
                print('Incorrect password.')
        else:
            print('Login not found.')
        return None

    def add_friend(self, user_id, friend_id):
        if user_id in self.users and friend_id in self.users:
            self.users[user_id].add_friend(self.users[friend_id])
            self.users[friend_id].add_friend(self.users[user_id])
            self.save_users()
            print('Friend added successfully.')
        else:
            print('One or both users do not exist on the network.')

    def remove_friend(self, user_id, friend_id):
        if user_id in self.users and friend_id in self.users:
            self.users[user_id].remove_friend(self.users[friend_id])
            self.users[friend_id].remove_friend(self.users[user_id])
            self.save_users()
            print('Friend removed successfully.')
        else:
            print('One or both users do not exist on the network.')

    def list_friends(self, user_id):
        if user_id in self.users:
            return self.users[user_id].list_friends(self.users)
        else:
            print('User not found.')

    def view_network(self):
        network = {}
        for user_id, user in self.users.items():
            network[user.name] = user.list_friends(self.users)
        return network

    def save_users(self):
        with open('users.json', 'w') as file:
            data = {user_id: user.to_dict() for user_id, user in self.users.items()}
            json.dump(data, file)

    def load_users(self):
        try:
            with open("users.json", "r") as file:
                data = json.load(file)
                for user_id, user_data in data.items():
                    user = User.from_dict(user_data)
                    self.users[user_id] = user
                    self.logins[user.login] = user_id
        except FileNotFoundError:
            pass

    def delete_account(self, user_id):
        if user_id in self.users:
            del self.logins[self.users[user_id].login]
            del self.users[user_id]
            self.save_users()
            print(f"Account deleted successfully for user ID {user_id}.")
        else:
            print("User not found.")

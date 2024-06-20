import re
import json
import inquirer

class User:
    def __init__(self, user_id, name, login, password):
        self.user_id = user_id
        self.name = name
        self.login = login
        self.password = password
        self.friends = set()

    def add_friend(self, friend):
        if friend.user_id == self.user_id:
            print('User cannot add themselves as a friend.')
        else:
            self.friends.add(friend.user_id)

    def remove_friend(self, friend):
        if friend.user_id in self.friends:
            self.friends.remove(friend.user_id)
        else:
            print('User is not a friend!')

    def list_friends(self, users):
        friend_list = [users[friend_id].name for friend_id in self.friends]
        return friend_list

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "login": self.login,
            "password": self.password,
            "friends": list(self.friends)
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["user_id"], data["name"], data["login"], data["password"])
        user.friends = set(data["friends"])
        return user

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

def create_new_id(network):
    return max(network.users.keys(), default=0) + 1

def renderMenu():
    choices = [
        "1️⃣  Create account",
        "2️⃣  Log in",
        "3️⃣  Add friend",
        "4️⃣  Remove friend",
        "5️⃣  List friends",
        "6️⃣  View network",
        "7️⃣  Logout"
    ]

    questions = [
        inquirer.List('menu',
                      message='Select an option:',
                      choices=choices),
    ]

    resposta = inquirer.prompt(questions)
    resposta = resposta['menu']
    resposta_numero = resposta.split(' ')[0][0]
    
    return str(resposta_numero)

def console_interface():
    network = SocialNetwork()
    user_id = None

    while True:
        print("\n--- iFace ---")
        option = renderMenu()

        if option == '1':
            print("\n--- Create account ---")
            name = input('Name: ')
            login = input('Email: ')
            while not network.validate_email(login):
                print("❌ Login must be a valid email containing '@'.")
                login = input('Email: ')
            password = input('Password: ')
            while not network.validate_password(password):
                print('❌ Password must contain at least one uppercase letter.')
                password = input('Password: ')
            user_id = create_new_id(network)
            network.create_account(user_id, name, login, password)

        elif option == '2':
            print("\n--- Log in ---")
            login = input("Email: ")
            password = input("Password: ")
            user_id = network.authenticate(login, password)

        elif option == '3':
            print("\n--- Add friend ---")
            if user_id:
                friend_choices = [
                    f"{user.user_id}: {user.name}" for uid, user in network.users.items() if uid != user_id and uid not in network.users[user_id].friends
                ]
                if friend_choices:
                    questions = [
                        inquirer.List('friend',
                                      message='Select a friend to add:',
                                      choices=friend_choices)
                    ]
                    answer = inquirer.prompt(questions)
                    friend_id = int(answer['friend'].split(':')[0])
                    network.add_friend(user_id, friend_id)
                else:
                    print("No available users to add as friends.")
            else:
                print("❌ You need to log in first.")

        elif option == '4':
            print("\n--- Remove friend ---")
            if user_id:
                friend_choices = [
                    f"{uid}: {network.users[uid].name}" for uid in network.users[user_id].friends
                ]
                if friend_choices:
                    questions = [
                        inquirer.List('friend',
                                      message='Select a friend to remove:',
                                      choices=friend_choices)
                    ]
                    answer = inquirer.prompt(questions)
                    friend_id = int(answer['friend'].split(':')[0])
                    network.remove_friend(user_id, friend_id)
                else:
                    print("No friends to remove.")
            else:
                print("❌ You need to log in first.")

        elif option == '5':
            print("\n--- List friends ---")
            if user_id:
                friends = network.list_friends(user_id)
                print(f"{network.users[user_id].name}'s friends: {', '.join(friends) if friends else 'No friends.'}")
            else:
                print("❌ You need to log in first.")

        elif option == '6':
            print("\n--- View network ---")
            network_view = network.view_network()
            for user, friends in network_view.items():
                print(f"{user}: {', '.join(friends) if friends else 'No friends.'}")

        elif option == '7':
            print("Logging out... 👋")
            break

        else:
            print('❌ Invalid option. Please try again.')

console_interface()

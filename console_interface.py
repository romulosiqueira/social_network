import inquirer
from social_network import SocialNetwork
from utils import create_new_id, render_menu

def console_interface():
    network = SocialNetwork()
    user_id = None

    while True:
        print("\n--- iFace ---")
        option = render_menu()

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
            print("\n--- Delete account ---")
            if user_id:
                confirm = input('Are you sure you want to delete your account? This action cannot be undone. (yes/no): ')
                if confirm.lower() == 'yes':
                    network.delete_account(user_id)
                    user_id = None
            else:
                print("❌ You need to log in first.")

        
        elif option == '8':
            print("Logging out... 👋")
            break

        else:
            print('❌ Invalid option. Please try again.')

if __name__ == "__main__":
    console_interface()

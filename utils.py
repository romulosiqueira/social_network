import inquirer
from social_network import SocialNetwork

def create_new_id(network):
    return max(network.users.keys(), default=0) + 1

def render_menu():
    choices = [
        "1️⃣  Create account",
        "2️⃣  Log in",
        "3️⃣  Add friend",
        "4️⃣  Remove friend",
        "5️⃣  List friends",
        "6️⃣  View network",
        "7️⃣  Delete account",
        "8️⃣  Logout"
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

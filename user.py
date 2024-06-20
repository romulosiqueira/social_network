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

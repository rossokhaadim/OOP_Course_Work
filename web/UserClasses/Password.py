from User import User
class Password(User):
    def change_password(self, password):
        self.password = password
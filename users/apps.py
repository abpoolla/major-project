from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    #label = 'any_unique_name'

    def ready(self):
        import users.signals

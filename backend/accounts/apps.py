from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    
    def ready(self):
        import accounts.signals  # Import the signals module to register signal handlers

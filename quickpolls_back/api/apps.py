from django.apps import AppConfig
from better_profanity import profanity

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

class PollsConfig(AppConfig):
    name = 'polls'

    def ready(self):
        profanity.load_censor_words_from_file('../utils/palavras_proibidas.txt')
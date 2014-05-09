from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.crypto import get_random_string
from phpass import PasswordHash
 

class WpTranslator(BasePasswordHasher):

    algorithm = 'phpass'

    def __init__(self):
        self.wp_hasher = PasswordHash()
    
    def salt(self):
        return get_random_string()

    def verify(self, password, encoded):
        return self.wp_hasher.check_password(password, encoded)

    def encode(self, password):
        return self.wp_hasher.hash_password(password)

    def safe_summary(self, encoded):
        return self.wp_hasher.portable_hasher




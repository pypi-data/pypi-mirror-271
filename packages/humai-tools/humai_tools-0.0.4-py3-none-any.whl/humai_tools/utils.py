from datetime import datetime
import uuid
import unidecode
from random import choices, randint
import requests

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_uuid():
    return str(uuid.uuid4())

def normalize(s):
    return unidecode.unidecode(s.lower().strip().replace(' ', '_'))

def generate_human_code():
    WORDS_URL = 'https://storage.googleapis.com/humai-datasets/nlp/borges_words.csv'
    words = requests.get(WORDS_URL).text.strip().split(',')
    return f"{choices(words)[0]}{''.join(str(randint(0,9)) for i in range(3))}"
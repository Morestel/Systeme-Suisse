import random
from faker import Faker
fake = Faker()

# Création des joueurs

class Joueur:
    def __init__(self):
        self.elo = random.randint(1000, 2500)
        self.nom = fake.name()
        
j1 = Joueur()
print(j1.nom)
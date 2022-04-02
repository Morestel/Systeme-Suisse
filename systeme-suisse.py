import random
from faker import Faker
import config as config
import copy

fake = Faker()

# Création des joueurs

class Joueur:
    def __init__(self):
        self.elo = random.randint(1000, 2500)
        self.nom = fake.name()
        self.victoire = 0
        self.defaite = 0
        self.adversaires = []
        
class Ladder:
    def __init__(self):
        self.round = 1
        

def remplir_liste_joueurs(liste_joueurs):
    '''Remplissage de la liste des joueurs'''
    for i in range(config.NOMBRE_JOUEUR):
        liste_joueurs.append(Joueur())
     
    
def match(joueur1, joueur2):
    '''Match entre deux joueurs - celui qui a le plus gros elo a plus de chance de gagner'''
    elo_joueur1 = joueur1.elo
    elo_joueur2 = joueur2.elo 
    # Systeme de base -> Un joueur avec un plus gros elo gagne
    # TODO Changer systeme
    if elo_joueur1 > elo_joueur2:
        joueur1.victoire += 1
        joueur2.defaite += 1
    else:
        joueur1.defaite += 1
        joueur2.victoire += 1
        

def matchmaking(liste_joueurs):
    '''Matchmaking entre tous les joueurs\n
    Renvoie une liste de tuples (joueur1, joueur2) donnant les prochains matchs'''
    liste = sorted(liste_joueurs, key=lambda x: x.victoire, reverse=True)
    matchs = []
    i = 0
    while liste: # Tant que la liste n'est pas vide
        i = 0
        # On verifie que les joueurs ne se soient pas deja affrontes
        j = i + 1
        while liste[j] in liste[i].adversaires:
            j += 1

        # Ils ne se sont pas affrontes : ils vont le faire
        matchs.append((liste[i], liste[j]))
        liste[i].adversaires.append(liste[j])
        liste[j].adversaires.append(liste[i])
        # On les enleve de la liste pour ne pas les reutiliser
        liste.pop(j)
        liste.pop(i)
    return matchs
        
        
def format_match(matchs, ladder):
    '''Formatte l'affichage des matchs'''  
    print("------------------------") 
    print("Round numero : ", ladder.round) 
    for match in matchs:
        info_joueur1 = match[0].nom + " (elo : " + str(match[0].elo) + ") " + "(" + str(match[0].victoire) + "-" + str(match[0].defaite) + ")"
        info_joueur2 = match[1].nom + " (elo : " + str(match[1].elo) + ") " + "(" + str(match[1].victoire) + "-" + str(match[1].defaite) + ")"
        print(info_joueur1, "vs", info_joueur2)
    print("------------------------\n")   


def main():
    
    liste_joueurs = []
    ladder = Ladder()
    remplir_liste_joueurs(liste_joueurs=liste_joueurs)
    match(joueur1=liste_joueurs[0], joueur2=liste_joueurs[1])
    matchs = matchmaking(liste_joueurs=liste_joueurs)
    format_match(matchs=matchs, ladder=ladder)
    
        
if __name__== "__main__":
    main()
  
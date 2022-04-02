import random
from faker import Faker
import config as config
import time
import itertools

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
    joueur1.adversaires.append(joueur2)
    joueur2.adversaires.append(joueur1)
    
def pair_valide(module):
    for i in range(0, len(module)-1):
        if module[i+1] in module[i].adversaires:
            return False # Ils se sont déjà affrontés on renvoie faux 
    # Aucun match n'a déjà été joué, c'est valide
    return True

def penalty(joueur1, joueur2):
    '''Fonction de pénalité pour une paire'''
    return (joueur1.victoire - joueur2.victoire)**2 # Elevé au carré pour avoir des nombres positifs

def somme_penalty(liste_joueurs):
    '''Somme des pénalités pour un module'''
    somme = 0
    for i in range(0, len(liste_joueurs)-1):
        somme += penalty(liste_joueurs[i], liste_joueurs[i+1])
    return somme
        
def tri_bulle(tab_score, tab_joueurs):
    '''Tri par bulle de deux tableaux liés'''
    n = len(tab_score)
    for i in range(n):
        for j in range(0, n-i-1):
            if tab_score[j] > tab_score[j+1] :
                tab_score[j], tab_score[j+1] = tab_score[j+1], tab_score[j]
                tab_joueurs[j], tab_joueurs[j+1] = tab_joueurs[j+1], tab_joueurs[j]
    return tab_score, tab_joueurs

def matchmaking(liste_joueurs):
    '''Matchmaking entre tous les joueurs\n
    Renvoie une liste de tuples (joueur1, joueur2) donnant les prochains matchs'''

    liste = sorted(liste_joueurs, key=lambda x: x.victoire, reverse=True)
    matchs = []
    penalty_module = []
    modules = list(itertools.permutations(liste, len(liste)))
   
    for module in modules:
       penalty_module.append(somme_penalty(module))
    
    # Une fois qu'on a tous les scores, on trie pour obtenir le minimum
    penalty_module, modules = tri_bulle(penalty_module, modules)
    i = 0
    module_valide = modules[i]
    while not pair_valide(module_valide):
        i += 1
        module_valide = modules[i]
        
    # On choisit le module avec le minimum c'est-à-dire le premier à condition qu'il soit valide
    for i in range(0, len(modules[0])-1):
        matchs.append((modules[0][i], modules[0][i+1]))
        
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

def afficher_ladder(liste_joueurs):
    '''Affiche le ladder'''
    print("Leaderboard :")
    liste_joueurs = sorted(liste_joueurs, key=lambda x: x.victoire, reverse=True)
    i = 1
    for joueur in liste_joueurs:
        print(str(i), ". ", joueur.nom, " (elo : ", joueur.elo, ") ", "(" , joueur.victoire, "-" , joueur.defaite, ")")
        i += 1
    print("\n")


def main():
    
    liste_joueurs = []
    ladder = Ladder()
    remplir_liste_joueurs(liste_joueurs=liste_joueurs)
    for i in range(0, config.NOMBRE_ROUND):
        matchs = matchmaking(liste_joueurs=liste_joueurs)
        format_match(matchs=matchs, ladder=ladder)
        for i in matchs:
            match(joueur1=i[0], joueur2=i[1])
        # Affichage du leaderboard à la suite des matchs
        afficher_ladder(liste_joueurs=liste_joueurs)
        ladder.round += 1
    
        
if __name__== "__main__":
    main()
  
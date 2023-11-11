import csv
import os
import sys
import time

import colorama
import random

from src.object.Card import Card
from src.object.Player import Player


def clear_console():
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")


# initialisation des imports et variable
colorama.init()
cards: list[Card] = []
active_player: Player
print("Lancement du jeu ..")

# initialisation des cartes:
with open('resources/premier_age.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)

    for row in reader:
        cards.append(Card(row[0], row[1], row[2]))

clear_console()
print("Lancement du Jeu ...")

# initialisation des joueurs
player1: Player = Player(input("Quel est le nom du premier joueur ? "))
active_player = player1

name = input("Quel est le nom du deuxième joueur ? ")
if name == player1.name:
    name += " (2)"
    print("Votre nom est déjà attribuer.. \nNouveau nom:", name, "!")
player2: Player = Player(name)

name2 = input("Quel est le nom du troisième joueur ? ")
if name2 == player1.name and name2 + " (2)" == player2.name:
    name2 += " (3)"
    print("Votre nom est déjà attribuer.. \nNouveau nom:", name2, "!")
elif name2 == player1.name or name2 == player2.name:
    print("Votre nom est déjà attribuer.. \nNouveau nom:", name2, "!")
    name2 += " (2)"
player3: Player = Player(name2)

time.sleep(3)
clear_console()

# initialisation des jeux
random.shuffle(cards)

player1.hand.extend(cards[:7])
cards = cards[7:]

player2.hand.extend(cards[:7])
cards = cards[7:]

player3.hand.extend(cards[:7])
cards = cards[7:]


def print_hand():
    print("Voici votre main:")
    for i in range(len(active_player.hand) - 1):
        print(" -", i + 1, "- ", active_player.hand[i].name)


def age_1_loop():
    clear_console()
    print_hand()

    print("\n1: Défausser")
    print("2: Jouer")
    action: str = input("Que voulez vous faire ? ")

    while action != "1" and action != "2":
        action = input("Veuillez choisir 1 pour Défausser ou 2 pour Jouer : ")

    if action == "1":
        clear_console()
        print_hand()
        action = input("Donnez le numéro de la carde que vous voulez défausser OU écrivez 'retour' pour revenir en "
                       "arrière !")


while len(player3.hand) > 1:
    age_1_loop()

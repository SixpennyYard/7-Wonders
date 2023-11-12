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
playing: bool = True
print("Lancement du jeu ..")

# initialisation des cartes:
with open('resources/premier_age.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)

    for row in reader:
        cards.append(Card(row[0], row[1], row[2], row[3]))

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
    name2 += " (2)"
    print("Votre nom est déjà attribuer.. \nNouveau nom:", name2, "!")
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
    for i in range(len(active_player.hand)):
        if active_player.hand[i].coast != "":
            print(" -", i + 1, "- ", active_player.hand[i].name, "[Coût]", active_player.hand[i].coast)
        else:
            print(" -", i + 1, "- ", active_player.hand[i].name, "[Coût] Aucun")


def get_next_active():
    global active_player
    if active_player == player1:
        active_player = player2
    elif active_player == player2:
        active_player = player3
    else:
        hand1: list[Card] = player1.hand[:]
        hand2: list[Card] = player2.hand[:]
        hand3: list[Card] = player3.hand[:]
        player1.hand = hand3
        player2.hand = hand1
        player3.hand = hand2
        active_player = player1


def print_playable_hand():
    for card in active_player.hand:
        if card.coast == "" or card.coast is None:
            active_player.playable_hand.append(card)
        else:
            card_coast = card.coast.split(" ")
            if card_coast[1] == "piece" and int(card_coast[0]) <= active_player.money:
                active_player.playable_hand.append(card)
            elif card_coast[1] == "bois" and int(card_coast[0]) <= active_player.count_wood():
                active_player.playable_hand.append(card)
            elif card_coast[1] == "brique" and int(card_coast[0]) <= active_player.count_brick():
                active_player.playable_hand.append(card)
            elif card_coast[1] == "or" and int(card_coast[0]) <= active_player.count_gold():
                active_player.playable_hand.append(card)
            elif card_coast[1] == "verre" and int(card_coast[0]) <= active_player.count_glass():
                active_player.playable_hand.append(card)
            elif card_coast[1] == "pierre" and int(card_coast[0]) <= active_player.count_stone():
                active_player.playable_hand.append(card)
            elif card_coast[1] == "papier" and int(card_coast[0]) <= active_player.count_paper():
                active_player.playable_hand.append(card)
            elif card_coast[1] == "soie" and int(card_coast[0]) <= active_player.count_silk():
                active_player.playable_hand.append(card)

    print("Voici ce que vous pouvez jouer:")
    for i in range(len(active_player.playable_hand)):
        if active_player.playable_hand[i].coast != "":
            print(" -", i + 1, "- ", active_player.playable_hand[i].name, "[Coût]",
                  active_player.playable_hand[i].coast)
        else:
            print(" -", i + 1, "- ", active_player.playable_hand[i].name, "[Coût] Aucun")


def can_play() -> bool:
    for card in active_player.hand:
        if card.coast == "" or card.coast is None:
            return True
        else:
            card_coast = card.coast.split(" ")
            if card_coast[1] == "piece" and int(card_coast[0]) <= active_player.money:
                return True
            elif card_coast[1] == "bois" and int(card_coast[0]) <= active_player.count_wood():
                return True
            elif card_coast[1] == "brique" and int(card_coast[0]) <= active_player.count_brick():
                return True
            elif card_coast[1] == "or" and int(card_coast[0]) <= active_player.count_gold():
                return True
            elif card_coast[1] == "verre" and int(card_coast[0]) <= active_player.count_glass():
                return True
            elif card_coast[1] == "pierre" and int(card_coast[0]) <= active_player.count_stone():
                return True
            elif card_coast[1] == "papier" and int(card_coast[0]) <= active_player.count_paper():
                return True
            elif card_coast[1] == "soie" and int(card_coast[0]) <= active_player.count_silk():
                return True
    return False


def age_1_loop():
    clear_console()
    print("TOUR DE _-=", active_player.name, "=-_")
    # Print la liste des cartes que le joueur possède, par couleur !!
    # active_player.{remplacer par la couleur en anglais}   c:
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
                       "arrière : ")

        while action != "retour" and (not action.isdigit() or int(action) < 1 or int(action) > len(active_player.hand)):
            action = input("Veuillez entrer 'retour' ou le numéro d'une de vos carte (numéro de 1 à "
                           + str(len(active_player.hand)) + ") : ")

        if action.isdigit():
            del active_player.hand[int(action) - 1]
            active_player.money += 2 + len(active_player.yellow)
        else:
            return
    else:
        # jouer une carte
        if not can_play():
            clear_console()
            print("Vous ne pouvez pas jouer...")
            time.sleep(2)
            return
        else:
            clear_console()
            print_playable_hand()
            action = input("Donnez le numéro de la carde que vous voulez jouer OU écrivez 'retour' pour revenir en "
                           "arrière : ")

            while action != "retour" and (
                    not action.isdigit() or int(action) < 1 or int(action) > len(active_player.playable_hand)):
                action = input("Veuillez entrer 'retour' ou le numéro d'une de vos carte (numéro de 1 à "
                               + str(len(active_player.playable_hand)) + ") : ")
            if action == "retour":
                return
            else:
                played: Card = active_player.playable_hand[int(action) - 1]
                active_player.hand.remove(played)
                if played.color == "r":
                    active_player.red.append(played)
                    active_player.playable_hand.clear()
                elif played.color == "b":
                    active_player.brown.append(played)
                    active_player.playable_hand.clear()
                elif played.color == "y":
                    active_player.yellow.append(played)
                    active_player.playable_hand.clear()
                elif played.color == "blue":
                    active_player.blue.append(played)
                    active_player.playable_hand.clear()
                elif played.color == "g":
                    active_player.green.append(played)
                    active_player.playable_hand.clear()
                elif played.color == "grey":
                    active_player.grey.append(played)
                    active_player.playable_hand.clear()

                if played.coast != "" and played.coast.split(" ")[1] == "piece":
                    active_player.money -= int(played.coast.split(" ")[0])

                # Ajouter la récompense au joueur si c'est de l'or ou autre c:

    get_next_active()


while len(player3.hand) > 1:
    age_1_loop()

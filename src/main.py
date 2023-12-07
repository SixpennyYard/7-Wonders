import csv
import os
import sys
import time

import random

from object.Card import Card
from object.Player import Player


def clear_console():
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")


# initialisation des imports et variable
age: int = 1
cards: list[Card] = []
discard: list[Card] = []
active_player: Player
playing: bool = True
print("Lancement du jeu ..")
merveille = []

# initialisation des cartes:
with open('resources/merveille.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)

    for row in reader:
        merveille.append([row[0], row[1], row[2], row[3]])


with open('resources/premier_age.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)

    for row in reader:
        cards.append(Card(row[0], row[1], row[2], row[3]))

clear_console()
print("Lancement du Jeu ...")

# initialisation des joueurs
player1: Player = Player(input("Quel est le nom du premier joueur ? "), random.choice(merveille))
active_player = player1

name = input("Quel est le nom du deuxième joueur ? ")
if name == player1.name:
    name += " (2)"
    print("Votre nom est déjà attribuer.. \nNouveau nom:", name, "!")
player2: Player = Player(name, random.choice(merveille))

name2 = input("Quel est le nom du troisième joueur ? ")
if name2 == player1.name and name2 + " (2)" == player2.name:
    name2 += " (3)"
    print("Votre nom est déjà attribuer.. \nNouveau nom:", name2, "!")
elif name2 == player1.name or name2 == player2.name:
    name2 += " (2)"
    print("Votre nom est déjà attribuer.. \nNouveau nom:", name2, "!")
player3: Player = Player(name2, random.choice(merveille))
players = (player1, player2, player3)
index = players.index(active_player)

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


def set_next_active():
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


def playable_hand(player: Player):
    for card in player.hand:
        if card.coast == "" or card.coast is None:
            player.playable_hand.append(card)
        else:
            card_coast = card.coast.split(" ")
            if card_coast[1] == "piece" and int(card_coast[0]) <= player.money:
                player.playable_hand.append(card)
            elif card_coast[1] == "bois" and int(card_coast[0]) <= (player.count_wood()
                                                                    or player.money > 2):
                player.playable_hand.append(card)
            elif card_coast[1] == "brique" and int(card_coast[0]) <= (player.count_brick()
                                                                      or player.money > 2):
                player.playable_hand.append(card)
            elif card_coast[1] == "or" and int(card_coast[0]) <= (player.count_gold()
                                                                  or player.money > 2):
                player.playable_hand.append(card)
            elif card_coast[1] == "verre" and int(card_coast[0]) <= (player.count_glass()
                                                                     or player.money > 2):
                player.playable_hand.append(card)
            elif card_coast[1] == "pierre" and int(card_coast[0]) <= (player.count_stone()
                                                                      or player.money > 2):
                player.playable_hand.append(card)
            elif card_coast[1] == "papier" and int(card_coast[0]) <= (player.count_paper()
                                                                      or player.money > 2):
                player.playable_hand.append(card)
            elif card_coast[1] == "soie" and int(card_coast[0]) <= (player.count_silk()
                                                                    or player.money > 2):
                player.playable_hand.append(card)


def print_playable_hand():
    playable_hand(active_player)
    print("Voici ce que vous pouvez jouer:")
    for i in range(len(active_player.playable_hand)):
        if active_player.playable_hand[i].color != "y":
            if active_player.playable_hand[i].coast != "":
                print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût]",
                      active_player.playable_hand[i].coast, "| [Offre]", active_player.playable_hand[i].offer)
            else:
                print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût] Aucun | [Offre]",
                      active_player.playable_hand[i].offer)
        else:
            if active_player.playable_hand[i].name == "Comptoir Ouest":
                if active_player == player1:
                    if active_player.playable_hand[i].coast != "":
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût]",
                              active_player.playable_hand[i].coast, "| [Offre] Bois:",
                              player2.count_wood(), ", Pierre(s):", player2.count_stone(), ", Brique(s):",
                              player2.count_brick(), ", Or:", player2.count_gold())
                    else:
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût] Aucun | [Offre] Bois:",
                              player2.count_wood(), ", Pierre(s):", player2.count_stone(), ", Brique(s):",
                              player2.count_brick(), ", Or:", player2.count_gold())
                elif active_player == player2:
                    if active_player.playable_hand[i].coast != "":
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût]",
                              active_player.playable_hand[i].coast, "| [Offre] Bois:",
                              player3.count_wood(), ", Pierre(s):", player3.count_stone(), ", Brique(s):",
                              player3.count_brick(), ", Or:", player3.count_gold())
                    else:
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût] Aucun | [Offre] Bois:",
                              player3.count_wood(), ", Pierre(s):", player3.count_stone(), ", Brique(s):",
                              player3.count_brick(), ", Or:", player3.count_gold())
                elif active_player == player3:
                    if active_player.playable_hand[i].coast != "":
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût]",
                              active_player.playable_hand[i].coast, "| [Offre] Bois:",
                              player1.count_wood(), ", Pierre(s):", player1.count_stone(), ", Brique(s):",
                              player1.count_brick(), ", Or:", player1.count_gold())
                    else:
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût] Aucun | [Offre] Bois:",
                              player1.count_wood(), ", Pierre(s):", player1.count_stone(), ", Brique(s):",
                              player1.count_brick(), ", Or:", player1.count_gold())
            elif active_player.playable_hand[i].name == "Comptoir Est":
                if active_player == player1:
                    if active_player.playable_hand[i].coast != "":
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût]",
                              active_player.playable_hand[i].coast, "| [Offre] Bois:",
                              player3.count_wood(), ", Pierre(s):", player3.count_stone(), ", Brique(s):",
                              player3.count_brick(), ", Or:", player3.count_gold())
                    else:
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût] Aucun | [Offre] Bois:",
                              player3.count_wood(), ", Pierre(s):", player3.count_stone(), ", Brique(s):",
                              player3.count_brick(), ", Or:", player3.count_gold())
                elif active_player == player2:
                    if active_player.playable_hand[i].coast != "":
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût]",
                              active_player.playable_hand[i].coast, "| [Offre] Bois:",
                              player1.count_wood(), ", Pierre(s):", player1.count_stone(), ", Brique(s):",
                              player1.count_brick(), ", Or:", player1.count_gold())
                    else:
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût] Aucun | [Offre] Bois:",
                              player1.count_wood(), ", Pierre(s):", player1.count_stone(), ", Brique(s):",
                              player1.count_brick(), ", Or:", player1.count_gold())
                elif active_player == player3:
                    if active_player.playable_hand[i].coast != "":
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût]",
                              active_player.playable_hand[i].coast, "| [Offre] Bois:",
                              player2.count_wood(), ", Pierre(s):", player2.count_stone(), ", Brique(s):",
                              player2.count_brick(), ", Or:", player2.count_gold())
                    else:
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût] Aucun | [Offre] Bois:",
                              player2.count_wood(), ", Pierre(s):", player2.count_stone(), ", Brique(s):",
                              player2.count_brick(), ", Or:", player2.count_gold())
            elif active_player.playable_hand[i].name == "Marche":
                if active_player == player1:
                    if active_player.playable_hand[i].coast != "":
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût]",
                              active_player.playable_hand[i].coast, "| [Offre] Verre(s):",
                              player3.count_glass() + player2.count_glass(), ", Papier(s):",
                              player3.count_paper() + player2.count_paper(), ", Soie(s):",
                              player3.count_silk() + player2.count_silk())
                    else:
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name,
                              "| [Coût] Aucun | [Offre] Verre(s):",
                              player3.count_glass() + player2.count_glass(), ", Papier(s):",
                              player3.count_paper() + player2.count_paper(), ", Soie(s):",
                              player3.count_silk() + player2.count_silk())
                elif active_player == player2:
                    if active_player.playable_hand[i].coast != "":
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût]",
                              active_player.playable_hand[i].coast, "| [Offre] Verre(s):",
                              player3.count_glass() + player1.count_glass(), ", Papier(s):",
                              player3.count_paper() + player1.count_paper(), ", Soie(s):",
                              player3.count_silk() + player1.count_silk())
                    else:
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name,
                              "| [Coût] Aucun | [Offre] Verre(s):",
                              player3.count_glass() + player1.count_glass(), ", Papier(s):",
                              player3.count_paper() + player1.count_paper(), ", Soie(s):",
                              player3.count_silk() + player1.count_silk())
                elif active_player == player3:
                    if active_player.playable_hand[i].coast != "":
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name, "| [Coût]",
                              active_player.playable_hand[i].coast, "| [Offre] Verre(s):",
                              player2.count_glass() + player1.count_glass(), ", Papier(s):",
                              player2.count_paper() + player1.count_paper(), ", Soie(s):",
                              player2.count_silk() + player1.count_silk())
                    else:
                        print(" -", i + 1, "- ", active_player.playable_hand[i].name,
                              "| [Coût] Aucun | [Offre] Verre(s):",
                              player2.count_glass() + player1.count_glass(), ", Papier(s):",
                              player2.count_paper() + player1.count_paper(), ", Soie(s):",
                              player2.count_silk() + player1.count_silk())


def can_play_split(card_coast: list[str], player):
    if card_coast[1] == "piece" and int(card_coast[0]) <= player.money:
        return True
    elif card_coast[1] == "bois" and (int(card_coast[0]) <= player.count_wood()
                                      or player.money > 2):
        return True
    elif card_coast[1] == "brique" and (int(card_coast[0]) <= player.count_brick()
                                        or player.money > 2):
        return True
    elif card_coast[1] == "or" and (int(card_coast[0]) <= player.count_gold()
                                    or player.money > 2):
        return True
    elif card_coast[1] == "verre" and int(card_coast[0]) <= (player.count_glass()
                                                             or player.money > 2):
        return True
    elif card_coast[1] == "pierre" and int(card_coast[0]) <= (player.count_stone()
                                                              or player.money > 2):
        return True
    elif card_coast[1] == "papier" and int(card_coast[0]) <= (player.count_paper()
                                                              or player.money > 2):
        return True
    elif card_coast[1] == "soie" and int(card_coast[0]) <= (player.count_silk()
                                                            or player.money > 2):
        return True


def can_play(player) -> bool:
    for card in player.hand:
        if card.coast == "" or card.coast is None:
            return True
        else:
            if "&" in card.coast:
                card_coasts: list[str] = card.coast.split(" & ")
                for card_coast in card_coasts:
                    can_play_split(card_coast, player)
            else:
                card_coast: list[str] = card.coast.split(" ")
                can_play_split(card_coast, player)
    return False


def print_resources():
    print("\n\nPièce:", active_player.money)
    print("_-=Cartes Marrons=-_")
    print("Bois:", active_player.count_wood(), "   |    Brique(s):", active_player.count_brick(), "   |    Pierre(s):",
          active_player.count_stone(), "   |    Or(s):", active_player.count_gold())
    print("\n_-=Cartes Grises=-_")
    print("Verre:", active_player.count_glass(), "   |    Papier(s):", active_player.count_paper(), "   |    Soie(s):",
          active_player.count_silk())

    woods: str = "Rien"
    briks: str = "Rien"
    stones: str = "Rien"
    golds: str = "Rien"
    glass: str = "Rien"
    papers: str = "Rien"
    silks: str = "Rien"
    for resource in active_player.yellow:
        if resource.name == "Comptoir Ouest":
            if active_player == player1:
                woods = str(player2.count_wood()) + " contre " + str(player2.count_wood()) + " pièces."
                briks = str(player2.count_brick()) + " contre " + str(player2.count_brick()) + " pièces."
                stones = str(player2.count_stone()) + " contre " + str(player2.count_stone()) + " pièces."
                golds = str(player2.count_gold()) + " contre " + str(player2.count_gold()) + " pièces."
            elif active_player == player2:
                woods = str(player3.count_wood()) + " contre " + str(player3.count_wood()) + " pièces."
                briks = str(player3.count_brick()) + " contre " + str(player3.count_brick()) + " pièces."
                stones = str(player3.count_stone()) + " contre " + str(player3.count_stone()) + " pièces."
                golds = str(player3.count_gold()) + " contre " + str(player3.count_gold()) + " pièces."
            elif active_player == player3:
                woods = str(player1.count_wood()) + " contre " + str(player1.count_wood()) + " pièces."
                briks = str(player1.count_brick()) + " contre " + str(player1.count_brick()) + " pièces."
                stones = str(player1.count_stone()) + " contre " + str(player1.count_stone()) + " pièces."
                golds = str(player1.count_gold()) + " contre " + str(player1.count_gold()) + " pièces."
        elif resource.name == "Comptoir Est":
            if active_player == player1:
                woods = str(player3.count_wood()) + " contre " + str(player3.count_wood()) + " pièces."
                briks = str(player3.count_brick()) + " contre " + str(player3.count_brick()) + " pièces."
                stones = str(player3.count_stone()) + " contre " + str(player3.count_stone()) + " pièces."
                golds = str(player3.count_gold()) + " contre " + str(player3.count_gold()) + " pièces."
            elif active_player == player2:
                woods = str(player1.count_wood()) + " contre " + str(player1.count_wood()) + " pièces."
                briks = str(player1.count_brick()) + " contre " + str(player1.count_brick()) + " pièces."
                stones = str(player1.count_stone()) + " contre " + str(player1.count_stone()) + " pièces."
                golds = str(player1.count_gold()) + " contre " + str(player1.count_gold()) + " pièces."
            elif active_player == player3:
                woods = str(player2.count_wood()) + " contre " + str(player2.count_wood()) + " pièces."
                briks = str(player2.count_brick()) + " contre " + str(player2.count_brick()) + " pièces."
                stones = str(player2.count_stone()) + " contre " + str(player2.count_stone()) + " pièces."
                golds = str(player2.count_gold()) + " contre " + str(player2.count_gold()) + " pièces."
        elif resource.name == "Marche":
            if active_player == player1:
                papers = (str(player3.count_paper() + player2.count_paper()) + " contre " +
                          str(player3.count_paper() + player2.count_paper()) + " pièces.")
                glass = (str(player3.count_glass() + player2.count_glass()) + " contre " +
                         str(player3.count_glass() + player2.count_glass()) + " pièces.")
                silks = (str(player3.count_silk() + player2.count_silk()) + " contre " +
                         str(player3.count_silk() + player2.count_silk()) + " pièces.")
            elif active_player == player2:
                woods = str(player1.count_wood()) + " contre " + str(player1.count_wood()) + " pièces."
                briks = str(player1.count_brick()) + " contre " + str(player1.count_brick()) + " pièces."
                stones = str(player1.count_stone()) + " contre " + str(player1.count_stone()) + " pièces."
                golds = str(player1.count_gold()) + " contre " + str(player1.count_gold()) + " pièces."
            elif active_player == player3:
                woods = str(player2.count_wood()) + " contre " + str(player2.count_wood()) + " pièces."
                briks = str(player2.count_brick()) + " contre " + str(player2.count_brick()) + " pièces."
                stones = str(player2.count_stone()) + " contre " + str(player2.count_stone()) + " pièces."
                golds = str(player2.count_gold()) + " contre " + str(player2.count_gold()) + " pièces."

    print("\n_-=Cartes Jaunes=-_")
    print("Bois:", woods, "   |    Brique(s):", briks, "   |    Pierre(s):", stones, "   |    Or(s):", golds)
    print("Verre:", glass, "   |    Papier(s):", papers, "   |    Soie(s):", silks)


def build_split_card(coast: str):
    if "bois" in coast.split(" ")[1] and active_player.count_wood() == 0:
        if active_player.has_yellow_card("Comptoire Est"):
            right: Player = players[(index + 1) % 3]
            if right.count_wood() > 0:
                active_player.money -= 1
        elif active_player.has_yellow_card("Comptoire Ouest"):
            left: Player = players[(index - 1) % 3]
            if left.count_wood() > 0:
                active_player.money -= 1
        else:
            active_player.money -= 2

    if "pierre" in coast.split(" ")[1] and active_player.count_stone() == 0:
        if active_player.has_yellow_card("Comptoire Est"):
            right: Player = players[(index + 1) % 3]
            if right.count_stone() > 0:
                active_player.money -= 1
        elif active_player.has_yellow_card("Comptoire Ouest"):
            left: Player = players[(index - 1) % 3]
            if left.count_stone() > 0:
                active_player.money -= 1
        else:
            active_player.money -= 2

    if "brique" in coast.split(" ")[1] and active_player.count_brick() == 0:
        if active_player.has_yellow_card("Comptoire Est"):
            right: Player = players[(index + 1) % 3]
            if right.count_brick() > 0:
                active_player.money -= 1
        elif active_player.has_yellow_card("Comptoire Ouest"):
            left: Player = players[(index - 1) % 3]
            if left.count_brick() > 0:
                active_player.money -= 1
        else:
            active_player.money -= 2

    if "or" in coast.split(" ")[1] and active_player.count_gold() == 0:
        if active_player.has_yellow_card("Comptoire Est"):
            right: Player = players[(index + 1) % 3]
            if right.count_gold() > 0:
                active_player.money -= 1
        elif active_player.has_yellow_card("Comptoire Ouest"):
            left: Player = players[(index - 1) % 3]
            if left.count_gold() > 0:
                active_player.money -= 1
        else:
            active_player.money -= 2

    if "papier" in coast.split(" ")[1] and active_player.count_paper() == 0:
        if active_player.has_yellow_card("Marche"):
            right: Player = players[(index + 1) % 3]
            left: Player = players[(index - 1) % 3]
            if right.count_brick() > 0:
                active_player.money -= 1
            elif left.count_brick() > 0:
                active_player.money -= 1
        else:
            active_player.money -= 2

    if "verre" in coast.split(" ")[1] and active_player.count_glass() == 0:
        if active_player.has_yellow_card("Marche"):
            right: Player = players[(index + 1) % 3]
            left: Player = players[(index - 1) % 3]
            if right.count_brick() > 0:
                active_player.money -= 1
            elif left.count_brick() > 0:
                active_player.money -= 1
        else:
            active_player.money -= 2

    if "soie" in coast.split(" ")[1] and active_player.count_silk() == 0:
        if active_player.has_yellow_card("Marche"):
            right: Player = players[(index + 1) % 3]
            left: Player = players[(index - 1) % 3]
            if right.count_brick() > 0:
                active_player.money -= 1
            elif left.count_brick() > 0:
                active_player.money -= 1
        else:
            active_player.money -= 2


def build_card(played):
    if played.coast != "":
        if "&" in played.coast:
            coasts: list[str] = played.coast.split(" & ")
            for coast in coasts:
                build_split_card(coast)
        else:
            build_split_card(played.coast)
    active_player.playable_hand.clear()


def print_player_card(player):
    """
    :param player: Joueur actif sur ce tour

    Affiche les cartes, par couleur, du joueur
    """
    print("_-= Jaune =-_")
    player.print_yellow()
    print("_-= Marron =-_")
    player.print_brown()
    print("_-= Gris =-_")
    player.print_grey()
    print("_-= Vert =-_")
    player.print_green()
    print("_-= Rouge =-_")
    player.print_red()
    print("_-= Bleu =-_")
    player.print_blue()


def can_construct_wonder() -> bool:
    resources = ("bois", "pierre", "verre", "soie", "papier", "brique")
    if active_player.palier == 1:
        cout = active_player.merveille[2].split(" | ")[0]
    if active_player.palier == 2:
        cout = active_player.merveille[2].split(" | ")[1]
    if active_player.palier == 3:
        cout = active_player.merveille[2].split(" | ")[2]
        for resource in resources :
            if resource in cout:
                pass

def print_merveille():
    i: int
    cout_age = active_player.merveille[2].split(" | ")
    offre_age = active_player.merveille[3].split(" | ")
    print(merveille[0])
    for i in range(len(cout_age)):
        print("l'amélioration du palier", i+1, "coûte : ", cout_age[i])
        print("l'amélioration du palier", i+1, "coûte : ", offre_age[i])

def age_loop():
    clear_console()
    print("TOUR DE _-=", active_player.name, "=-_")
    print_merveille()
    print_player_card(active_player)
    print_resources()
    time.sleep(2)
    print_hand()

    print("\n1: Défausser")
    print("2: Jouer")
    print("3: Construire une merveille")
    action: str = input("Que voulez vous faire ? ")

    while action != "1" and action != "2" and action != "3":
        action = input("Veuillez choisir 1 pour Défausser ou 2 pour Jouer ou 3 pour construire une merveille : ")

    if action == "1":
        clear_console()
        print_hand()
        action = input(f"Donnez le numéro de la carde que vous voulez défauser OU écrivez 'retour' pour revenir en "
                       "arrière : ")
        while action != "retour" and (
                not action.isdigit() or int(action) < 1 or int(action) > len(active_player.hand)):
            action = input("Veuillez entrer 'retour' ou le numéro d'une de vos carte (numéro de 1 à "
                           + str(len(active_player.hand)) + ") : ")

        if action.isdigit():
            discard.append(active_player.hand[int(action) - 1])
            del active_player.hand[int(action) - 1]
            active_player.money += 2 + len(active_player.yellow)
            set_next_active()
        else:
            return
    elif action == "2":
        # jouer une carte
        if not can_play(active_player):
            clear_console()
            print("Vous ne pouvez pas jouer...")
            time.sleep(2)
            return
        else:
            clear_console()
            print_playable_hand()

            action = input(f"Donnez le numéro de la carde que vous voulez jouer OU écrivez 'retour' pour revenir en "
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
                    build_card(played)
                    active_player.red.append(played)

                elif played.color == "b":
                    build_card(played)
                    active_player.brown.append(played)

                elif played.color == "y":
                    build_card(played)
                    active_player.yellow.append(played)

                elif played.color == "blue":
                    build_card(played)
                    active_player.blue.append(played)

                elif played.color == "g":
                    build_card(played)
                    active_player.green.append(played)

                elif played.color == "grey":
                    build_card(played)
                    active_player.grey.append(played)

                if played.coast != "" and played.coast.split(" ")[1] == "piece":
                    build_card(played)
                    active_player.money -= int(played.coast.split(" ")[0])
                set_next_active()
    else:
        if not can_construct_wonder():
            return


while len(player3.hand) > 1:
    age_loop()


def count_war_point(adding_war: int):
    player1_war_point: int = 0
    for red_card in player1.red:
        player1_war_point += int(red_card.offer[0])

    player2_war_point: int = 0
    for red_card in player2.red:
        player2_war_point += int(red_card.offer[0])

    player3_war_point: int = 0
    for red_card in player3.red:
        player3_war_point += int(red_card.offer[0])

    if player1_war_point > player2_war_point:
        player1.war_point += adding_war
        player2.war_point -= 1
    else:
        player1.war_point -= 1
        player2.war_point += adding_war

    if player1_war_point > player3_war_point:
        player1.war_point += adding_war
        player3.war_point -= 1
    else:
        player1.war_point -= 1
        player3.war_point += adding_war

    if player3_war_point > player2_war_point:
        player3.war_point += adding_war
        player2.war_point -= 1
    else:
        player3.war_point -= 1
        player2.war_point += adding_war


count_war_point(1)
discard.clear()

clear_console()
print("L'Age 2 va commencer dans quelques instant..")
age += 1
time.sleep(2)

# initialisation des jeux
# TODO: Faire les enchainages...
with open('resources/deuxieme_age.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)

    for row in reader:
        if len(row) < 5:
            cards.append(Card(row[0], row[1], row[2], row[3]))
        else:
            cards.append(Card(row[0], row[1], row[2], row[3], row[4]))

random.shuffle(cards)
player1.hand.extend(cards[:7])
cards = cards[7:]
player2.hand.extend(cards[:7])
cards = cards[7:]
player3.hand.extend(cards[:7])
cards = cards[7:]

while len(player3.hand) > 1:
    age_loop()

count_war_point(3)
discard.clear()

clear_console()
print("L'Age 3 va commencer dans quelques instant..")
age += 1
time.sleep(2)

# initialisation des jeux
with open('resources/troisieme_age.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)

    for row in reader:
        cards.append(Card(row[0], row[1], row[2], row[3]))

random.shuffle(cards)
player1.hand.extend(cards[:7])
cards = cards[7:]
player2.hand.extend(cards[:7])
cards = cards[7:]
player3.hand.extend(cards[:7])
cards = cards[7:]

while len(player3.hand) > 1:
    age_loop()

count_war_point(5)
discard.clear()


# TODO: Compter les points des carte guilde et de la science !
def final_score_blue(player: Player):
    score_blue = 0
    for card in player.blue:
        score_blue += int(card.offer[0])
    return score_blue


def final_score_red(player: Player):
    return player.war_point


def final_score_yellow(player: Player):
    point: int = 0
    named_yellow: list[list[str, str]] = [["Port", "marron"], ["Phare", "marron"],
                                          ["Chambre de Commerce", "marron"], ["Arene", "marron"]]
    for card in named_yellow:
        if player.has_yellow_card(card[0]):
            if card[1] == "marron":
                point += len(player.brown)
            elif card[1] == "yellow":
                point += len(player.yellow)
            elif card[1] == "girs":
                point += len(player.grey) * 2
            else:
                point += 0  # TODO: 1 * le nombre d'etage de merveille construite.
    return point


def final_score_money(player: Player):
    return player.money // 3


def final_score_green(player: Player):
    green_symbole: list[str] = []
    green_score = 0
    for card in player.green:
        green_symbole.append(card.offer)
    nb_engrenage = green_symbole.count("Engrenage")
    nb_tablette = green_symbole.count("Tablette")
    nb_compas = green_symbole.count("Compas")
    if nb_engrenage == 1:
        green_score += 1
    elif nb_engrenage == 2:
        green_score += 4
    elif nb_engrenage == 3:
        green_score += 9
    elif nb_engrenage == 4:
        green_score += 16
    if nb_tablette == 1:
        green_score += 1
    elif nb_tablette == 2:
        green_score += 4
    elif nb_tablette == 3:
        green_score += 9
    elif nb_tablette == 4:
        green_score += 16
    if nb_compas == 1:
        green_score += 1
    elif nb_compas == 2:
        green_score += 4
    elif nb_compas == 3:
        green_score += 9
    elif nb_compas == 4:
        green_score += 16
    return green_score


def final_score(player: Player):
    return (final_score_yellow(player) + final_score_blue(player) + final_score_green(player)
            + final_score_money(player) + final_score_red(player))


def age():
    return age

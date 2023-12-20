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
merveille_player = random.choice(merveille)
merveille.remove(merveille_player)
player1: Player = Player(input("Quel est le nom du premier joueur ? "), merveille_player)
active_player = player1

name = input("Quel est le nom du deuxième joueur ? ")
merveille_player = random.choice(merveille)
merveille.remove(merveille_player)
if name == player1.name:
    name += " (2)"
    print("Votre nom est déjà attribuer.. \nNouveau nom:", name, "!")
player2: Player = Player(name, merveille_player)

name2 = input("Quel est le nom du troisième joueur ? ")
if name2 == player1.name and name2 + " (2)" == player2.name:
    name2 += " (3)"
    print("Votre nom est déjà attribuer.. \nNouveau nom:", name2, "!")
elif name2 == player1.name or name2 == player2.name:
    name2 += " (2)"
    print("Votre nom est déjà attribuer.. \nNouveau nom:", name2, "!")
    merveille_player = random.choice(merveille)
    merveille.remove(merveille_player)
player3: Player = Player(name2, merveille_player)
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
        if card.coast == "" or card.coast is None or player.free_bat == 1:
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
    if played.coast != "" or active_player.free_bat == 1:
        if "&" in played.coast:
            coasts: list[str] = played.coast.split(" & ")
            for coast in coasts:
                build_split_card(coast)
        else:
            build_split_card(played.coast)
    active_player.playable_hand.clear()
    if played.coast != "" and active_player.has_free_bat:
        active_player.free_bat -= 1


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
    for resource in resources:
        if resource in cout:
            player_resource = active_player.count_resource(resource)
            if int(cout[0]) <= player_resource:
                return True
            else:
                x = int(cout[0]) - player_resource
                if active_player.money >= x * 2:
                    return True
    return False


def build_wonder():
    resources = ("bois", "pierre", "verre", "soie", "papier", "brique")
    if active_player.palier == 1:
        cout = active_player.merveille[2].split(" | ")[0]
    if active_player.palier == 2:
        cout = active_player.merveille[2].split(" | ")[1]
    if active_player.palier == 3:
        cout = active_player.merveille[2].split(" | ")[2]
    for resource in resources:
        if resource in cout:
            player_resource = active_player.count_resource(resource)
            if int(cout[0]) <= player_resource:
                offre = active_player.merveille[3].split(" | ")[active_player.palier - 1]
                active_player.palier += 1
                if "culture" in offre:
                    active_player.culture += int(offre[0])
                elif "guerre" in offre:
                    active_player.war += int(offre[0])
                elif "piece" in offre:
                    active_player.money += int(offre[0])
                elif "free_bat" in offre:
                    active_player.free_bat += 1
                    active_player.has_free_bat = True
                elif "resource" in offre:
                    active_player.cheating_resource
                elif "defausse" in offre:
                    for card in discard:
                        print(card.name, card.offer)
                elif "vert" in offre:
                    choice = input("tablette(1), compas(2), engrenage(3) : ")
                    while int(choice) != 1 or int(choice) != 2 or int(choice) != 3:
                        choice = input("tablette(1), compas(2), engrenage(3) : ")
                    if choice == 1:
                        active_player.symbole = "tablette"
                    if choice == 2:
                        active_player.symbole = "compas"
                    if choice == 3:
                        active_player.symbole = "engrenage"
            else:
                x = int(cout[0]) - player_resource
                if active_player.money >= x * 2:
                    offre = active_player.merveille[3].split(" | ")[active_player.palier - 1]
                    active_player.palier += 1
                    active_player.money -= x * 2
                    if "culture" in offre:
                        active_player.culture += int(offre[0])
                    elif "guerre" in offre:
                        active_player.war += int(offre[0])
                    elif "piece" in offre:
                        active_player.money += int(offre[0])
                    elif "free_bat" in offre:
                        active_player.free_bat += 1
                        active_player.has_free_bat = True
    return False


def print_merveille():
    cout_age = active_player.merveille[2].split(" | ")
    offre_age = active_player.merveille[3].split(" | ")
    print(f"Votre merveille est: {active_player.merveille[0]}\nVous êtes au palier n°{active_player.palier}/3\n\n")
    print("l'amélioration du palier", active_player.palier, "coûte : ", cout_age[active_player.palier - 1])
    print("")
    print("l'amélioration du palier", active_player.palier, "offre : ", offre_age[active_player.palier - 1])
    print("")
    print("")


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
            active_player.money += 2 + len(active_player.yellow)
            clear_console()
            print(f"Vous venez de défausser la carte {active_player.hand[int(action) - 1].name};"
                  f"\n    elle offrait: {active_player.hand[int(action) - 1].offer}"
                  f"\n    elle coutait: {active_player.hand[int(action) - 1].coast}"
                  f"\n\nVous avez maintenant {active_player.money} pièces")
            del active_player.hand[int(action) - 1]
            time.sleep(7)
            set_next_active()
        else:
            return
    elif action == "2":
        # jouer une carte
        if not can_play(active_player):
            clear_console()
            print("Vous ne pouvez pas jouer...")
            time.sleep(3)
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
                clear_console()
                if played.name == "Port":
                    active_player.money += len(active_player.brown)
                elif played.name == "Phare":
                    active_player.money += len(active_player.yellow)
                elif played.name == "Arene":
                    active_player.money += 1 * (active_player.palier - 1)
                print(f"Vous venez de construire la carte {played.name} qui vous offre {played.offer}."
                      f"\nVous avez {active_player.money} pièce(s).")
                time.sleep(7)
                set_next_active()
    else:
        if can_construct_wonder():
            clear_console()
            print("Vous allez devoir choisir la carte à défausser pour construire votre merveille !")
            time.sleep(4)
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
                clear_console()
                print(f"Vous venez de défausser la carte {active_player.hand[int(action) - 1].name};"
                      f"\n    elle offrait: {active_player.hand[int(action) - 1].offer}"
                      f"\n    elle coutait: {active_player.hand[int(action) - 1].coast}"
                      f"\n\nVous avez maintenant {active_player.money} pièces")
                del active_player.hand[int(action) - 1]
                time.sleep(4)
            else:
                return
            build_wonder()
            clear_console()
            print(f"Vous venez de construire le palier n°{active_player.palier - 1} de la merveille "
                  f"{active_player.merveille[0]}.\nVous avez {active_player.money} pièce(s).")
            time.sleep(7)
            set_next_active()
        else:
            clear_console()
            print("Vous ne pouvez pas construire de merveille...")
            time.sleep(3)
            return


while len(player3.hand) > 1:
    age_loop()

if player1.has_free_bat:
    player1.free_bat = 1
if player2.has_free_bat:
    player2.free_bat = 1
if player3.has_free_bat:
    player3.free_bat = 1


def count_war_point(adding_war: int):
    player1_war_point: int = 0
    for red_card in player1.red:
        player1_war_point += int(red_card.offer[0]) + player1.war

    player2_war_point: int = 0
    for red_card in player2.red:
        player2_war_point += int(red_card.offer[0]) + player2.war

    player3_war_point: int = 0
    for red_card in player3.red:
        player3_war_point += int(red_card.offer[0]) + player3.war

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
with open('resources/deuxieme_age.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)

    for row in reader:
        if len(row) < 5:
            cards.append(Card(row[0], row[1], row[2], row[3]))
        else:
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


def final_score_blue(player: Player):
    score_blue = 0
    for card in player.blue:
        score_blue += int(card.offer[0])
    return score_blue + player.culture


def final_score_red(player: Player):
    return player.war_point


def final_score_yellow(player: Player):
    point: int = 0
    named_yellow: list[list[str, str]] = [["Port", "marron"], ["Phare", "marron"],
                                          ["Chambre de Commerce", "marron"], ["Arene", "marron"],
                                          ["Guilde des artisans", "gris"], ["Guilde des philosophe", "vert"],
                                          ["Guilde des espions", "rouge"], ["Guilde des magistrats", "bleu"]]
    for card in named_yellow:
        if player.has_yellow_card(card[0]):
            if card[1] == "marron":
                point += len(player.brown)
            elif card[1] == "yellow":
                point += len(player.yellow)
            elif card[1] == "gris":
                point += len(player.grey)
            elif card[1] == "vert":
                point += len(player.grey)
            elif card[1] == "rouge":
                point += len(player.grey)
            elif card[1] == "bleu":
                point += len(player.grey)
            else:
                point += 1 * (player.palier - 1)
    return point


def final_score_money(player: Player):
    return player.money // 3


def fianl_score_green():
    green_score = 0
    green_score1 = 0
    green_score2 = 0
    green_score3 = 0
    nb_engrenage = 3
    nb_tablette = 2
    nb_compas = 1
    i = 0
    test1 = 0
    test2 = 0
    test3 = 0
    while i < 3:
        if i == 0:
            nb_engrenage += 1
            green_score1 += green_score_fonc(nb_engrenage, nb_tablette, nb_compas)
            nb_engrenage -= 1
            i += 1
        elif i == 1:
            nb_tablette += 1
            green_score2 += green_score_fonc(nb_engrenage, nb_tablette, nb_compas)
            nb_tablette -= 1
            i += 1
        elif i == 2:
            nb_compas += 1
            green_score3 += green_score_fonc(nb_engrenage, nb_tablette, nb_compas)
            nb_compas -= 1
            i += 1
    if green_score1 >= green_score2 and green_score1 >= green_score3:
        green_score = green_score1
    elif green_score2 >= green_score1 and green_score2 >= green_score3:
        green_score = green_score2
    else:
        green_score = green_score3
    return green_score


def green_score_fonc(nb_engrenage, nb_tablette, nb_compas):
    green_scoreok = 0
    if nb_engrenage == 1:
        green_scoreok += 1
    elif nb_engrenage == 2:
        green_scoreok += 4
    elif nb_engrenage == 3:
        green_scoreok += 9
    elif nb_engrenage == 4:
        green_scoreok += 16
    if nb_tablette == 1:
        green_scoreok += 1
    elif nb_tablette == 2:
        green_scoreok += 4
    elif nb_tablette == 3:
        green_scoreok += 9
    elif nb_tablette == 4:
        green_scoreok += 16
    if nb_compas == 1:
        green_scoreok += 1
    elif nb_compas == 2:
        green_scoreok += 4
    elif nb_compas == 3:
        green_scoreok += 9
    elif nb_compas == 4:
        green_scoreok += 16

    while nb_engrenage > 0 and nb_tablette > 0 and nb_compas > 0:
        nb_engrenage -= 1
        nb_tablette -= 1
        nb_compas -= 1
        green_scoreok += 7

    return green_scoreok


def final_score(player: Player):
    return (final_score_yellow(player) + final_score_blue(player) + final_score_green(player)
            + final_score_money(player) + final_score_red(player))

players_score = [[player1, final_score(player1)], [player1, final_score(player2)], [player1, final_score(player3)]]
players_score.sort(key=lambda x: x[1], reverse=True)
clear_console()
print("Voici les scores !")

time.sleep(1)
print("En premier....")
print(players_score[0][0].name, "avec un score de:", players_score[0][1])

time.sleep(3)
print("En deuxieme....")
print(players_score[1][0].name, "avec un score de:", players_score[1][1])

print("Et pour finir en dernier :'(")
print(players_score[2][0].name, "avec un score de:", players_score[2][1])

def age():
    return age

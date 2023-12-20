from copy import copy
from math import sqrt

from src import main
from src.object import Card, Player


def algo_build_split_card(coast: str, player: Player):
    index = main.players.index(player)
    if "bois" in coast.split(" ")[1] and player.count_wood() == 0:
        if player.has_yellow_card("Comptoire Est"):
            right: Player = main.players[(index + 1) % 3]
            if right.count_wood() > 0:
                player.money -= 1
        elif player.has_yellow_card("Comptoire Ouest"):
            left: Player = main.players[(index - 1) % 3]
            if left.count_wood() > 0:
                player.money -= 1
        else:
            player.money -= 2

    if "pierre" in coast.split(" ")[1] and player.count_stone() == 0:
        if player.has_yellow_card("Comptoire Est"):
            right: Player = main.players[(index + 1) % 3]
            if right.count_stone() > 0:
                player.money -= 1
        elif player.has_yellow_card("Comptoire Ouest"):
            left: Player = main.players[(index - 1) % 3]
            if left.count_stone() > 0:
                player.money -= 1
        else:
            player.money -= 2

    if "brique" in coast.split(" ")[1] and player.count_brick() == 0:
        if player.has_yellow_card("Comptoire Est"):
            right: Player = main.players[(index + 1) % 3]
            if right.count_brick() > 0:
                player.money -= 1
        elif player.has_yellow_card("Comptoire Ouest"):
            left: Player = main.players[(index - 1) % 3]
            if left.count_brick() > 0:
                player.money -= 1
        else:
            player.money -= 2

    if "or" in coast.split(" ")[1] and player.count_gold() == 0:
        if player.has_yellow_card("Comptoire Est"):
            right: Player = main.players[(index + 1) % 3]
            if right.count_gold() > 0:
                player.money -= 1
        elif player.has_yellow_card("Comptoire Ouest"):
            left: Player = main.players[(index - 1) % 3]
            if left.count_gold() > 0:
                player.money -= 1
        else:
            player.money -= 2

    if "papier" in coast.split(" ")[1] and player.count_paper() == 0:
        if player.has_yellow_card("Marche"):
            right: Player = main.players[(index + 1) % 3]
            left: Player = main.players[(index - 1) % 3]
            if right.count_brick() > 0:
                player.money -= 1
            elif left.count_brick() > 0:
                player.money -= 1
        else:
            player.money -= 2

    if "verre" in coast.split(" ")[1] and player.count_glass() == 0:
        if player.has_yellow_card("Marche"):
            right: Player = main.players[(index + 1) % 3]
            left: Player = main.players[(index - 1) % 3]
            if right.count_brick() > 0:
                player.money -= 1
            elif left.count_brick() > 0:
                player.money -= 1
        else:
            player.money -= 2

    if "soie" in coast.split(" ")[1] and player.count_silk() == 0:
        if player.has_yellow_card("Marche"):
            right: Player = main.players[(index + 1) % 3]
            left: Player = main.players[(index - 1) % 3]
            if right.count_brick() > 0:
                player.money -= 1
            elif left.count_brick() > 0:
                player.money -= 1
        else:
            player.money -= 2


def algo_build_card(played, player: Player):
    if played.coast != "":
        if "&" in played.coast:
            coasts: list[str] = played.coast.split(" & ")
            for coast in coasts:
                algo_build_split_card(coast, player)
        else:
            algo_build_split_card(played.coast, player)
    player.playable_hand.clear()


def evaluate_state(player: Player):
    return main.final_score(player) + player.evaluate_ressources() * sqrt(main.age())


def minimax(depth, player: Player, player_action, maximizing_player):
    if depth == 0:
        return evaluate_state(player)

    if maximizing_player:
        best_state_eval: int = 0
        if player_action == "Défausser":
            if main.can_play(player):
                main.playable_hand(player)
                for card in player.playable_hand:
                    previous_score: int = main.final_score(player)
                    previous_state_eval: int = evaluate_state(player)
                    _copy_player: Player = copy(player)
                    _copy_player.money += 2 + len(_copy_player.yellow)
                    after_score: int = main.final_score(_copy_player)
                    after_state_eval: int = evaluate_state(_copy_player)
                    if after_score > after_state_eval >= previous_state_eval and after_score >= previous_score:
                        best_state_eval = after_state_eval
                        for action_s in _possible_moves():
                            minimax(depth - 1, _copy_player, action_s, maximizing_player)
                    else:
                        continue
        elif player_action == "Jouer":
            for card in player.playable_hand:
                _copy_player: Player = copy(player)
                previous_score: int = main.final_score(player)
                previous_state_eval: int = evaluate_state(player)
                algo_build_card(card, _copy_player)
                after_score: int = main.final_score(_copy_player)
                after_state_eval: int = evaluate_state(_copy_player)
                if after_score > after_state_eval >= previous_state_eval and after_score >= previous_score:
                    best_state_eval = after_state_eval
                    for action_s in _possible_moves():
                        minimax(depth - 1, _copy_player, action_s, maximizing_player)
                else:
                    continue
        else:
            best_state_eval = 0
        return best_state_eval
    else:
        pass


def _possible_moves():
    return ['Jouer', 'Défausser', 'Merveille']


depth_limit = 6
best_eval: float = 0
best_action = None

for action in _possible_moves():
    eval = minimax(depth_limit, main.active_player, action, True)
    if eval > best_eval:
        best_eval = eval
        best_action = action

print("Meilleur coup à jouer:", best_action)

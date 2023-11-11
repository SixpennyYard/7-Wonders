from src.object.Card import Card


class Player:
    def __init__(self, name: str, money: int = 3):
        self.name = name
        self.money = money
        self.hand: list[Card] = []

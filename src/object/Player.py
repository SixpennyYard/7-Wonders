from object.Card import Card


class Player:
    def __init__(self, name: str, money: int = 3):
        self.playable_hand: list[Card] = []
        self.yellow: list[Card] = []
        self.brown: list[Card] = []
        self.grey: list[Card] = []
        self.green: list[Card] = []
        self.red: list[Card] = []
        self.blue: list[Card] = []
        self.name = name
        self.money = money
        self.hand: list[Card] = []

    def count_wood(self) -> int:
        count: int = 0
        for resource in self.brown:
            if resource.offer.split(" ")[1] == "bois":
                count += 1

        return count

    def count_brick(self) -> int:
        count: int = 0
        for resource in self.brown:
            if resource.offer.split(" ")[1] == "brique":
                count += 1

        return count

    def count_gold(self) -> int:
        count: int = 0
        for resource in self.brown:
            if resource.offer.split(" ")[1] == "or":
                count += 1

        return count

    def count_stone(self) -> int:
        count: int = 0
        for resource in self.brown:
            if resource.offer.split(" ")[1] == "pierre":
                count += 1

        return count

    def count_glass(self) -> int:
        count: int = 0
        for resource in self.grey:
            if resource.offer.split(" ")[1] == "verre":
                count += 1

        return count

    def count_paper(self) -> int:
        count: int = 0
        for resource in self.grey:
            if resource.offer.split(" ")[1] == "papier":
                count += 1

        return count

    def count_silk(self) -> int:
        count: int = 0
        for resource in self.grey:
            if resource.offer.split(" ")[1] == "soie":
                count += 1

        return count

    def get_yellow(self, card_name: str) -> bool:
        """
        :param card_name: Prend le nom d'une carte jaune en paramètre
        :return: renvoie True si le joueur la possède sinon false
        """
        for card in self.yellow:
            if card.name == card_name:
                return True
        return False

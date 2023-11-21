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

    def get_yellow_card(self, card_name: str) -> bool:
        """
        :param card_name: Prend le nom d'une carte jaune en paramètre
        :return: renvoie True si le joueur la possède sinon false
        """
        for card in self.yellow:
            if card.name == card_name:
                return True
        return False

    def print_yellow(self):
        for i in self.yellow:
            print(f"Nom: {i.name}\nCoût: {i.coast if i.coast != "" else "Aucun"}\nOffre: {i.offer}"
                  f"\nBatiment précédent: {i.free_offer if i.free_offer != "" else "Aucun"}\n\n")

    def print_brown(self):
        for i in self.brown:
            print(f"Nom: {i.name}\nCoût: {i.coast if i.coast != "" else "Aucun"}\nOffre: {i.offer}"
                  f"\nBatiment précédent: {i.free_offer if i.free_offer != "" else "Aucun"}\n\n")

    def print_grey(self):
        for i in self.grey:
            print(f"Nom: {i.name}\nCoût: {i.coast if i.coast != "" else "Aucun"}\nOffre: {i.offer}"
                  f"\nBatiment précédent: {i.free_offer if i.free_offer != "" else "Aucun"}\n\n")

    def print_green(self):
        for i in self.green:
            print(f"Nom: {i.name}\nCoût: {i.coast if i.coast != "" else "Aucun"}\nOffre: {i.offer}"
                  f"\nBatiment précédent: {i.free_offer if i.free_offer != "" else "Aucun"}\n\n")

    def print_red(self):
        for i in self.red:
            print(f"Nom: {i.name}\nCoût: {i.coast if i.coast != "" else "Aucun"}\nOffre: {i.offer}"
                  f"\nBatiment précédent: {i.free_offer if i.free_offer != "" else "Aucun"}\n\n")

    def print_blue(self):
        for i in self.blue:
            print(f"Nom: {i.name}\nCoût: {i.coast if i.coast != "" else "Aucun"}\nOffre: {i.offer}"
                  f"\nBatiment précédent: {i.free_offer if i.free_offer != "" else "Aucun"}\n\n")

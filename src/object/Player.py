from object.Card import Card


class Player:
    def __init__(self, name: str, merveille, money: int = 3):
        self.playable_hand: list[Card] = []
        self.yellow: list[Card] = []
        self.brown: list[Card] = []
        self.grey: list[Card] = []
        self.green: list[Card] = []
        self.red: list[Card] = []
        self.blue: list[Card] = []
        self.purple: list[Card] = []
        self.name = name
        self.money = money
        self.hand: list[Card] = []
        self.war_point: int = 0
        self.yellow_point: int = 0
        self.merveille = merveille
        self.palier = 1

    def count_wood(self) -> int:
        count: int = 0
        for resource in self.brown:
            if resource.offer.split(" ")[1] == "bois":
                count += 1
        for resource in self.yellow:
            if "bois" in resource.offer:
                count += 1
        if self.merveille[1] == "bois":
            count += 1

        return count

    def count_brick(self) -> int:
        count: int = 0
        for resource in self.brown:
            if resource.offer.split(" ")[1] == "brique":
                count += 1
        for resource in self.yellow:
            if "brique" in resource.offer:
                count += 1
        if self.merveille[1] == "brique":
            count += 1

        return count

    def count_gold(self) -> int:
        count: int = 0
        for resource in self.brown:
            if resource.offer.split(" ")[1] == "or":
                count += 1
        for resource in self.yellow:
            if "or" in resource.offer:
                count += 1
        if self.merveille[1] == "or":
            count += 1

        return count

    def count_stone(self) -> int:
        count: int = 0
        for resource in self.brown:
            if resource.offer.split(" ")[1] == "pierre":
                count += 1
        for resource in self.yellow:
            if "pierre" in resource.offer:
                count += 1
        if self.merveille[1] == "pierre":
            count += 1

        return count

    def count_glass(self) -> int:
        count: int = 0
        for resource in self.grey:
            if resource.offer.split(" ")[1] == "verre":
                count += 1
        for resource in self.yellow:
            if "verre" in resource.offer:
                count += 1
        if self.merveille[1] == "verre":
            count += 1

        return count

    def count_paper(self) -> int:
        count: int = 0
        for resource in self.grey:
            if resource.offer.split(" ")[1] == "papier":
                count += 1
        for resource in self.yellow:
            if "papier" in resource.offer:
                count += 1
        if self.merveille[1] == "papier":
            count += 1

        return count

    def count_silk(self) -> int:
        count: int = 0
        for resource in self.grey:
            if resource.offer.split(" ")[1] == "soie":
                count += 1
        for resource in self.yellow:
            if "soie" in resource.offer:
                count += 1
        if self.merveille[1] == "soie":
            count += 1

        return count

    def count_resource(self, resource: str):
        if resource == "bois":
            return self.count_wood()
        elif resource == "soie":
            return self.count_silk()
        elif resource == "papier":
            return self.count_paper()
        elif resource == "verre":
            return self.count_glass()
        elif resource == "brique":
            return self.count_brick()
        elif resource == "pierre":
            return self.count_stone()

    def evaluate_ressources(self) -> int:
        evaluation: int = 0
        resources: tuple = (
            self.count_silk(), self.count_gold(), self.count_brick(), self.count_wood(), self.count_stone(),
            self.count_glass(), self.count_paper()
        )
        for resource in resources:
            if resource >= 3:
                evaluation -= 2
            else:
                evaluation += resource
        return evaluation

    def has_yellow_card(self, card_name: str) -> bool:
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

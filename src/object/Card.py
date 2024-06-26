class Card:
    def __init__(self, name: str, cost: str, offer: str, color: str, free_offer: str = ""):
        """
        :param name: Nom de la carte
        :param cost: Coût de la carte
        :param offer: Ce que la carte offre
        :param color: Couleur de la carte
        :param free_offer: Les possibles chaînage de la carte pour la construire
        """
        self.name = name
        self.cost = cost
        self.offer = offer
        self.color = color
        self.free_offer = free_offer

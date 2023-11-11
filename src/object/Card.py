class Card:
    def __init__(self, name: str, coast: str, offer: str, free_offer: str = ""):
        """
        :param name: Nom de la carte
        :param coast: Coût de la carte
        :param offer: Ce que la carte offre
        :param free_offer: Les possibles enchaînage de la carte pour la construire
        """
        self.name = name
        self.coast = coast
        self.offer = offer
        self.free_offer = free_offer

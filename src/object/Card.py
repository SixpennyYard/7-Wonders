class Card:
    def __init__(self, name, coast, offer, next_age_offer):
        """
        :param name: Nom de la carte
        :param coast: Coût de la carte
        :param offer: Ce que la carte offre
        :param next_age_offer: Les possibles enchaînage de la carte pour l'âge suivant
        """
        self.name = name
        self.coast = coast
        self.offer = offer
        self.next_age_offer = next_age_offer

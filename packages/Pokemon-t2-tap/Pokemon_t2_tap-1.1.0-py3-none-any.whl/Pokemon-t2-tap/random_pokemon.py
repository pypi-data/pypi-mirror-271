import pkg_resources
import pandas as pd

class RandomPokemon:
    FILE_PATH = pkg_resources.resource_filename(__name__, 'pokemon.csv')

    def __init__(self):
        self._file = pd.read_csv(RandomPokemon.FILE_PATH)
        self._pokemon = None
        self._number = None
        self._name = None
        self._type1 = None
        self._type2 = None
        self._hp = None
        self._attack = None
        self._defense = None
        self._sp_attack = None
        self._sp_defense = None
        self._speed = None
        self._total = None
        self._generation = None
        self._legendary = None

    def generate_random(self):
        self._pokemon = self._file.sample().iloc[0]
        self._number = self._pokemon["#"]
        self._name = self._pokemon["Name"]
        self._type1 = self._pokemon["Type 1"]
        self._type2 = self._pokemon["Type 2"]
        self._hp = self._pokemon["HP"]
        self._attack = self._pokemon["Attack"]
        self._defense = self._pokemon["Defense"]
        self._sp_attack = self._pokemon["Sp. Atk"]
        self._sp_defense = self._pokemon["Sp. Def"]
        self._speed = self._pokemon["Speed"]
        self._total = self._pokemon["Total"]
        self._generation = self._pokemon["Generation"]
        self._legendary = self._pokemon["Legendary"]

    def getPokemon(self):
        return self._pokemon

    def getNumber(self):
        return self._number

    def getName(self):
        return self._name

    def getType1(self):
        return self._type1

    def getType2(self):
        return self._type2

    def getHP(self):
        return self._hp

    def getAttack(self):
        return self._attack

    def getDefense(self):
        return self._defense

    def getSpecialAttack(self):
        return self._sp_attack

    def getSpecialDefense(self):
        return self._sp_defense

    def getSpeed(self):
        return self._speed

    def getTotal(self):
        return self._total

    def getGeneration(self):
        return self._generation

    def isLegendary(self):
        return self._legendary

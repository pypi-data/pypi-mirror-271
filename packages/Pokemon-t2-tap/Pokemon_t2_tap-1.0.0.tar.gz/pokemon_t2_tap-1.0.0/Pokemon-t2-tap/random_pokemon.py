import pkg_resources
import pandas as pd

class RandomPokemon:
    FILE_PATH = pkg_resources.resources_filiename(__name__, 'pokemon.csv')

    def __init__(self):
        self._file = pd.read_csv(RandomPokemon.FILE_PATH)
        self._pokemon = None
        self._number = None
        self._name = None
        self._type = None

    def generate_random(self):
        self._pokemon = self._file.sample()
        self._number = self._pokemon['#'].values[0]
        self._name = self._pokemon['Name'].values[0]
        self._type = self._pokemon['Type 1'].values[0]

    def getPokemon(self):
        return self._pokemon

    def getNumber(self):
        return self._number

    def getName(self):
        return self._name

    def getType1(self):
        return self._type1
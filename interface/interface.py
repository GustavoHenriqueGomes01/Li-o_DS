from abc import ABC, abstractmethod

class PokemonInterface(ABC):

    @abstractmethod
    def cadastrar(self, pokemon):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def consultar(self, nome):
        pass

    @abstractmethod
    def atualizar(self, id, pokemon):
        pass

    @abstractmethod
    def deletar(self, id):
        pass
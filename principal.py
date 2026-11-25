import tkinter as tk

from repositor.Banco_de_dados import PokemonRepository
from visualizar.tela_principal import TelaPrincipal


def iniciar_sistema():

    root = tk.Tk()

    repository = PokemonRepository()

    app = TelaPrincipal(root, repository)

    def fechar_sistema():
        repository.fechar_conexao()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", fechar_sistema)

    root.mainloop()


if __name__ == "__main__":
    iniciar_sistema()
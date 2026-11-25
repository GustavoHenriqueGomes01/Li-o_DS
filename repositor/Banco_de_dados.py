
import sqlite3

from interface.interface import PokemonInterface
from classes.Classes import Pokemon


class PokemonRepository(PokemonInterface):

    def __init__(self):
        self.conexao = sqlite3.connect("pokedex.db")
        self.criar_tabela()

    def criar_tabela(self):

        cursor = self.conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pokemons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                tipo TEXT NOT NULL,
                altura REAL,
                peso REAL,
                descricao TEXT,
                imagem BLOB
            )
        """)

        self.conexao.commit()

    def cadastrar(self, pokemon):

        cursor = self.conexao.cursor()

        cursor.execute("""
            INSERT INTO pokemons
            (nome, tipo, altura, peso, descricao, imagem)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            pokemon.nome,
            pokemon.tipo,
            pokemon.altura,
            pokemon.peso,
            pokemon.descricao,
            pokemon.imagem
        ))

        self.conexao.commit()

        pokemon.id = cursor.lastrowid

        return pokemon.id

    def listar(self):

        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT * FROM pokemons
            ORDER BY nome
        """)

        resultados = cursor.fetchall()

        pokemons = []

        for linha in resultados:

            pokemon = Pokemon(
                id=linha[0],
                nome=linha[1],
                tipo=linha[2],
                altura=linha[3],
                peso=linha[4],
                descricao=linha[5],
                imagem=linha[6]
            )

            pokemons.append(pokemon)

        return pokemons

    def consultar(self, nome):

        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT * FROM pokemons
            WHERE nome LIKE ?
            ORDER BY nome
        """, (f"%{nome}%",))

        resultados = cursor.fetchall()

        pokemons = []

        for linha in resultados:

            pokemon = Pokemon(
                id=linha[0],
                nome=linha[1],
                tipo=linha[2],
                altura=linha[3],
                peso=linha[4],
                descricao=linha[5],
                imagem=linha[6]
            )

            pokemons.append(pokemon)

        return pokemons

    def atualizar(self, id, pokemon):

        cursor = self.conexao.cursor()

        cursor.execute("""
            UPDATE pokemons
            SET nome = ?,
                tipo = ?,
                altura = ?,
                peso = ?,
                descricao = ?,
                imagem = ?
            WHERE id = ?
        """, (
            pokemon.nome,
            pokemon.tipo,
            pokemon.altura,
            pokemon.peso,
            pokemon.descricao,
            pokemon.imagem,
            id
        ))

        self.conexao.commit()

        return cursor.rowcount > 0

    def deletar(self, id):

        cursor = self.conexao.cursor()

        cursor.execute("""
            DELETE FROM pokemons
            WHERE id = ?
        """, (id,))

        self.conexao.commit()

        return cursor.rowcount > 0

    def fechar_conexao(self):

        if self.conexao:
            self.conexao.close()

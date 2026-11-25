import sqlite3

from interface.interface import PokemonInterface
from classes.Classes import Pokemon


class PokemonRepository(PokemonInterface):

    def __init__(self):
        self.conexao = sqlite3.connect("pokedex.db")
        self.conexao.execute("PRAGMA foreign_keys = ON")
        self.criar_tabela()

    def criar_tabela(self):

        cursor = self.conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pokemons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                tipo TEXT NOT NULL,
                altura REAL NOT NULL,
                peso REAL NOT NULL,
                descricao TEXT,
                imagem BLOB NOT NULL
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

    def listar(self):

        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT * FROM pokemons ORDER BY nome
        """)

        registros = cursor.fetchall()

        return [
            Pokemon(
                id=r[0],
                nome=r[1],
                tipo=r[2],
                altura=r[3],
                peso=r[4],
                descricao=r[5],
                imagem=r[6]
            )
            for r in registros
        ]

    def consultar(self, nome):

        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT * FROM pokemons
            WHERE nome LIKE ?
            ORDER BY nome
        """, (f"%{nome}%",))

        registros = cursor.fetchall()

        return [
            Pokemon(
                id=r[0],
                nome=r[1],
                tipo=r[2],
                altura=r[3],
                peso=r[4],
                descricao=r[5],
                imagem=r[6]
            )
            for r in registros
        ]

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
            DELETE FROM pokemons WHERE id = ?
        """, (id,))

        self.conexao.commit()

        return cursor.rowcount > 0

    def fechar(self):
        self.conexao.close()
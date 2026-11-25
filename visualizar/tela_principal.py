import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

from classes.Classes import Pokemon
from api.imagem import ImagemService


class TelaPrincipal:

    def __init__(self, root, repository):

        self.root = root
        self.repository = repository
        self.imagem_service = ImagemService()

        self.id_selecionado = None
        self.imagem_bytes = None
        self.imagem_tk = None

        self.root.title("Pokédex - Cadastro de Pokémons")
        self.root.geometry("1050x720")
        self.root.configure(bg="#f2f2f2")
        self.root.minsize(900, 650)

        self.criar_interface()
        self.listar_pokemons()

    def criar_interface(self):

        titulo = tk.Label(
            self.root,
            text="POKÉDEX",
            font=("Arial", 26, "bold"),
            bg="#cc0000",
            fg="white",
            pady=15
        )

        titulo.pack(fill="x")

        principal = tk.Frame(
            self.root,
            bg="#f2f2f2"
        )

        principal.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        formulario = tk.LabelFrame(
            principal,
            text="Dados do Pokémon",
            font=("Arial", 12, "bold"),
            bg="#f2f2f2",
            padx=15,
            pady=15
        )

        formulario.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        tk.Label(
            formulario,
            text="Nome:",
            bg="#f2f2f2"
        ).pack(anchor="w")

        self.nome_entry = tk.Entry(formulario, width=40)
        self.nome_entry.pack(fill="x", pady=5)

        tk.Label(
            formulario,
            text="Tipo:",
            bg="#f2f2f2"
        ).pack(anchor="w")

        self.tipo_entry = tk.Entry(formulario)
        self.tipo_entry.pack(fill="x", pady=5)

        tk.Label(
            formulario,
            text="Altura (metros):",
            bg="#f2f2f2"
        ).pack(anchor="w")

        self.altura_entry = tk.Entry(formulario)
        self.altura_entry.pack(fill="x", pady=5)

        tk.Label(
            formulario,
            text="Peso (kg):",
            bg="#f2f2f2"
        ).pack(anchor="w")

        self.peso_entry = tk.Entry(formulario)
        self.peso_entry.pack(fill="x", pady=5)

        tk.Label(
            formulario,
            text="Descrição:",
            bg="#f2f2f2"
        ).pack(anchor="w")

        self.descricao_entry = tk.Text(
            formulario,
            height=3,
            width=40
        )

        self.descricao_entry.pack(fill="x", pady=5)

        tk.Button(
            formulario,
            text="Buscar imagem na PokéAPI",
            bg="#3366cc",
            fg="white",
            command=self.buscar_imagem
        ).pack(fill="x", pady=5)

        botoes = tk.Frame(
            formulario,
            bg="#f2f2f2"
        )

        botoes.pack(fill="x", pady=10)

        tk.Button(
            botoes,
            text="Cadastrar",
            bg="#28a745",
            fg="white",
            command=self.cadastrar
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=3
        )

        tk.Button(
            botoes,
            text="Atualizar",
            bg="#ff9800",
            fg="white",
            command=self.atualizar
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=3
        )

        tk.Button(
            botoes,
            text="Excluir",
            bg="#cc0000",
            fg="white",
            command=self.excluir
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=3
        )

        tk.Button(
            formulario,
            text="Limpar campos",
            command=self.limpar
        ).pack(fill="x", pady=5)

        # Prévia menor e posicionada depois dos botões para evitar que
        # os controles fiquem escondidos em telas com pouca altura.
        self.imagem_container = tk.Frame(
            formulario,
            bg="white",
            width=180,
            height=180,
            relief="solid",
            bd=1
        )

        self.imagem_container.pack(pady=5)
        self.imagem_container.pack_propagate(False)

        self.imagem_label = tk.Label(
            self.imagem_container,
            text="Imagem do Pokémon",
            bg="white",
            fg="#777777"
        )

        self.imagem_label.pack(
            fill="both",
            expand=True
        )

        consulta = tk.LabelFrame(
            principal,
            text="Pokémons cadastrados",
            font=("Arial", 12, "bold"),
            bg="#f2f2f2",
            padx=10,
            pady=10
        )

        consulta.pack(
            side="right",
            fill="both",
            expand=True,
            padx=10
        )

        tk.Label(
            consulta,
            text="Pesquisar pelo nome:",
            bg="#f2f2f2"
        ).pack(anchor="w")

        self.pesquisa_entry = tk.Entry(consulta)
        self.pesquisa_entry.pack(fill="x", pady=5)

        tk.Button(
            consulta,
            text="Consultar",
            command=self.consultar
        ).pack(fill="x", pady=5)

        tk.Button(
            consulta,
            text="Mostrar todos",
            command=self.listar_pokemons
        ).pack(fill="x", pady=5)

        self.lista = tk.Listbox(
            consulta,
            font=("Arial", 11),
            height=22
        )

        self.lista.pack(
            fill="both",
            expand=True,
            pady=10
        )

        self.lista.bind(
            "<<ListboxSelect>>",
            self.selecionar_pokemon
        )

    def buscar_imagem(self):

        nome = self.nome_entry.get().strip()

        if not nome:
            messagebox.showwarning(
                "Atenção",
                "Digite o nome do Pokémon."
            )
            return

        try:

            imagem = self.imagem_service.buscar_imagem(nome)

            if not imagem:
                raise ValueError("Imagem não encontrada.")

            self.imagem_bytes = imagem

            self.exibir_imagem(imagem)

            messagebox.showinfo(
                "Sucesso",
                "Imagem encontrada com sucesso!"
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível buscar a imagem: {erro}"
            )

    def exibir_imagem(self, imagem_bytes):

        if not imagem_bytes:
            self.imagem_label.config(
                image="",
                text="Imagem não disponível"
            )
            self.imagem_tk = None
            return

        try:
            imagem = Image.open(
                BytesIO(imagem_bytes)
            ).convert("RGBA")

            # Redimensiona sem cortar ou deformar o Pokémon
            largura_maxima = 170
            altura_maxima = 170

            try:
                filtro = Image.Resampling.LANCZOS
            except AttributeError:
                filtro = Image.LANCZOS

            imagem.thumbnail(
                (largura_maxima, altura_maxima),
                filtro
            )

            self.imagem_tk = ImageTk.PhotoImage(imagem)

            self.imagem_label.config(
                image=self.imagem_tk,
                text=""
            )

        except Exception as erro:
            self.imagem_label.config(
                image="",
                text="Não foi possível carregar a imagem"
            )
            self.imagem_tk = None
            raise erro

    def obter_pokemon(self):

        nome = self.nome_entry.get().strip()
        tipo = self.tipo_entry.get().strip()
        altura = self.altura_entry.get().strip()
        peso = self.peso_entry.get().strip()

        descricao = self.descricao_entry.get(
            "1.0",
            tk.END
        ).strip()

        if not nome or not tipo or not altura or not peso:

            messagebox.showwarning(
                "Atenção",
                "Preencha todos os campos obrigatórios."
            )

            return None

        try:

            altura = float(altura.replace(",", "."))
            peso = float(peso.replace(",", "."))

            if altura <= 0 or peso <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Erro",
                "Altura e peso devem ser números maiores que zero."
            )

            return None

        if not self.imagem_bytes:

            messagebox.showwarning(
                "Atenção",
                "Busque a imagem do Pokémon na PokéAPI."
            )

            return None

        return Pokemon(
            nome=nome,
            tipo=tipo,
            altura=altura,
            peso=peso,
            descricao=descricao,
            imagem=self.imagem_bytes
        )

    def cadastrar(self):

        pokemon = self.obter_pokemon()

        if pokemon is None:
            return

        try:

            self.repository.cadastrar(pokemon)

            messagebox.showinfo(
                "Sucesso",
                "Pokémon cadastrado com sucesso!"
            )

            self.limpar()
            self.listar_pokemons()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível cadastrar: {erro}"
            )

    def listar_pokemons(self):

        self.lista.delete(0, tk.END)

        try:

            pokemons = self.repository.listar()

            for pokemon in pokemons:

                texto = (
                    f"ID: {pokemon.id} | "
                    f"{pokemon.nome} | "
                    f"{pokemon.tipo}"
                )

                self.lista.insert(tk.END, texto)

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível listar: {erro}"
            )

    def consultar(self):

        nome = self.pesquisa_entry.get().strip()

        self.lista.delete(0, tk.END)

        if not nome:
            self.listar_pokemons()
            return

        try:

            pokemons = self.repository.consultar(nome)

            for pokemon in pokemons:

                texto = (
                    f"ID: {pokemon.id} | "
                    f"{pokemon.nome} | "
                    f"{pokemon.tipo}"
                )

                self.lista.insert(tk.END, texto)

            if not pokemons:

                messagebox.showinfo(
                    "Consulta",
                    "Nenhum Pokémon encontrado."
                )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível consultar: {erro}"
            )

    def selecionar_pokemon(self, evento):

        selecao = self.lista.curselection()

        if not selecao:
            return

        try:

            texto = self.lista.get(selecao[0])

            id_pokemon = int(
                texto.split("|")[0].replace("ID:", "").strip()
            )

            pokemons = self.repository.listar()

            pokemon = next(
                (p for p in pokemons if p.id == id_pokemon),
                None
            )

            if pokemon is None:
                return

            self.id_selecionado = pokemon.id

            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, pokemon.nome)

            self.tipo_entry.delete(0, tk.END)
            self.tipo_entry.insert(0, pokemon.tipo)

            self.altura_entry.delete(0, tk.END)
            self.altura_entry.insert(0, str(pokemon.altura))

            self.peso_entry.delete(0, tk.END)
            self.peso_entry.insert(0, str(pokemon.peso))

            self.descricao_entry.delete("1.0", tk.END)

            self.descricao_entry.insert(
                "1.0",
                pokemon.descricao or ""
            )

            self.imagem_bytes = pokemon.imagem

            self.exibir_imagem(pokemon.imagem)

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível selecionar o Pokémon: {erro}"
            )

    def atualizar(self):

        if self.id_selecionado is None:

            messagebox.showwarning(
                "Atenção",
                "Selecione um Pokémon na lista."
            )

            return

        pokemon = self.obter_pokemon()

        if pokemon is None:
            return

        try:

            sucesso = self.repository.atualizar(
                self.id_selecionado,
                pokemon
            )

            if sucesso:

                messagebox.showinfo(
                    "Sucesso",
                    "Pokémon atualizado com sucesso!"
                )

                self.limpar()
                self.listar_pokemons()

            else:

                messagebox.showwarning(
                    "Atenção",
                    "Pokémon não encontrado."
                )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível atualizar: {erro}"
            )

    def excluir(self):

        if self.id_selecionado is None:

            messagebox.showwarning(
                "Atenção",
                "Selecione um Pokémon para excluir."
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir este Pokémon?"
        )

        if not confirmar:
            return

        try:

            sucesso = self.repository.deletar(
                self.id_selecionado
            )

            if sucesso:

                messagebox.showinfo(
                    "Sucesso",
                    "Pokémon excluído com sucesso!"
                )

                self.limpar()
                self.listar_pokemons()

            else:

                messagebox.showwarning(
                    "Atenção",
                    "Pokémon não encontrado."
                )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível excluir: {erro}"
            )

    def limpar(self):

        self.id_selecionado = None
        self.imagem_bytes = None
        self.imagem_tk = None

        self.nome_entry.delete(0, tk.END)
        self.tipo_entry.delete(0, tk.END)
        self.altura_entry.delete(0, tk.END)
        self.peso_entry.delete(0, tk.END)

        self.descricao_entry.delete(
            "1.0",
            tk.END
        )

        self.pesquisa_entry.delete(0, tk.END)

        self.imagem_label.config(
            image="",
            text="Imagem do Pokémon"
        )

        self.lista.selection_clear(0, tk.END)
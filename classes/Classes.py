
class Pokemon:

    def __init__(
        self,
        nome,
        tipo,
        altura,
        peso,
        descricao,
        imagem=None,
        id=None
    ):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.altura = altura
        self.peso = peso
        self.descricao = descricao
        self.imagem = imagem

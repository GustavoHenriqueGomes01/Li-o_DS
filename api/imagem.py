import requests


class ImagemService:

    def buscar_imagem(self, nome):

        nome = nome.strip().lower()

        url = f"https://pokeapi.co/api/v2/pokemon/{nome}"

        try:

            resposta = requests.get(url, timeout=10)
            resposta.raise_for_status()

            dados = resposta.json()

            imagem_url = (
                dados["sprites"]["other"]["official-artwork"]["front_default"]
                or dados["sprites"]["front_default"]
            )

            if not imagem_url:
                raise ValueError("Imagem não encontrada.")

            imagem = requests.get(imagem_url, timeout=10)
            imagem.raise_for_status()

            return imagem.content

        except requests.RequestException:
            raise Exception(
                "Não foi possível acessar a PokéAPI. "
                "Verifique sua conexão com a internet."
            )

        except (KeyError, TypeError):
            raise Exception("Não foi possível encontrar a imagem.")
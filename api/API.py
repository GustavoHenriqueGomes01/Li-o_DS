
import requests


class ImagemService:

    def buscar_imagem(self, nome):

        if not nome or not nome.strip():
            raise ValueError("Informe o nome do Pokémon.")

        nome = nome.strip().lower()

        url = f"https://pokeapi.co/api/v2/pokemon/{nome}"

        try:

            resposta = requests.get(
                url,
                timeout=10
            )

            resposta.raise_for_status()

            dados = resposta.json()

            imagem_url = dados["sprites"]["front_default"]

            if not imagem_url:
                raise ValueError(
                    "Este Pokémon não possui imagem disponível."
                )

            imagem = requests.get(
                imagem_url,
                timeout=10
            )

            imagem.raise_for_status()

            return imagem.content

        except requests.exceptions.HTTPError as erro:

            if erro.response is not None and erro.response.status_code == 404:
                raise ValueError("Pokémon não encontrado na PokéAPI.")

            raise Exception("Erro ao consultar a PokéAPI.")

        except requests.exceptions.Timeout:
            raise Exception("Tempo limite de conexão excedido.")

        except requests.exceptions.ConnectionError:
            raise Exception("Verifique sua conexão com a internet.")

        except requests.exceptions.RequestException:
            raise Exception("Não foi possível baixar a imagem.")


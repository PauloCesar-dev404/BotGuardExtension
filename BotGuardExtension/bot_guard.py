import requests
from .err import *
from .ws import WsClient

class BotGuardClient:
    """
    Cliente para utilizar o BotGuard, permitindo obter respostas a partir de um bytecode.
    """

    def __init__(self):
        """
        Inicializa o BotGuardClient.

        Args:
            saved (bool, optional): Parâmetro opcional indicando se há dados salvos (cache ou estado).
        """


    def get_bot_guard_reponse(self, program: str, identifier: str =None) -> dict:
        """
        Obtém a resposta do BotGuard a partir de um bytecode.

        Args:
            program (str): Bytecode a ser processado pela máquina virtual, utilizado para obter permissões de ações no YouTube.
            identifier (str): Identificador para a sessão ou requisição EX: (ID do vídeo  ou visitorId).

        Returns:
            dict: Resposta processada pelo BotGuard.

        Raises:
            InvalidByteCode: Se o bytecode estiver inválido ou expirado.
            Exception: Se a resposta contiver um erro.
        """
        client = WsClient(bytecode=program, identifier=identifier)
        client.start()
        response = client.get_message()
        if program == response or not program:
            raise InvalidByteCode('O bytecode está inválido ou expirado!')
        if 'error' in response:
            raise Exception(response)
        return response

    @staticmethod
    def __send_request(headers: dict, endpoint: str, payload: list = None):
        return requests.post(url=endpoint, json=payload, headers=headers)

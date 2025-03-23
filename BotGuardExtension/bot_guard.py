import requests
from .err import *
from .ws import WsClient

class BotGuardClient:
    """
    Cliente para utilizar o BotGuard, permitindo obter respostas a partir de um bytecode.
    """

    def __init__(self,timeout:int=5):
        """
        Inicializa o BotGuardClient.

        Args:
            timeout (int, optional): Tempo de espera da resposta.Padrão é 5s
        """
        self.__timeout = timeout

    def get_bot_guard_reponse(self, program: str, identifier: str = '') -> dict:
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
        client = WsClient(bytecode=program,
                          identifier=identifier,
                          timeout=self.__timeout)
        client.start()
        response = client.get_message()
        if program == response or not program:
            raise InvalidByteCode('O bytecode está inválido ou expirado!')
        if program in response.get('bot_guard_response',''):
            raise InvalidByteCode(
                'O bytecode está inválido ou expirado!'
            )
        if response.get('error',''):
            raise WsClientError(response.get('error'))
        return response



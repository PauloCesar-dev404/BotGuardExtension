import signal
import sys
import websocket
import asyncio
import json
import threading
import websockets
from colorama import Fore, Style, init
from datetime import datetime
connected_clients = {}
connected_clients_valid = ['browser', 'APP']
init(autoreset=True)
def log_message(message: str, type: str = ''):
    """
    Gera logs formatados contendo data, hora e a mensagem.

    Args:
        message (str): Mensagem a ser exibida.
        type (str, optional): Tipo do log (INFO, ERROR, etc.). Valor padrão é ''.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_log = f"[{Fore.LIGHTYELLOW_EX}{timestamp}{Style.RESET_ALL}] {message}"
    print(formatted_log)
class WsClient:
    def __init__(self, bytecode: str, identifier: str = ''):
        """
        Inicializa o cliente com o bytecode e um identificador.

        Args:
            bytecode (str): Bytecode ou programa a ser enviado.
            identifier (str): Identificador usado para correlacionar a resposta.
        """
        self.__identifier = identifier
        self.__bytecode = bytecode
        self.__adr = "ws://localhost:9090"  # Endereço do WebSocket Server
        self.__mensagem = ''  # Armazena a mensagem recebida

        # Configuração do WebSocket com callbacks para eventos
        self.__ws = websocket.WebSocketApp(
            self.__adr,
            on_open=self.__on_open,
            on_message=self.__on_message,
            on_error=self.__on_error,
            on_close=self.__on_close
        )

    def __on_open(self, ws):
        """
        Callback executado quando a conexão WebSocket é aberta.

        Envia a identificação do cliente e o bytecode para o servidor.
        """
        self.__ws.send(json.dumps({'client_id': 'APP'}))
        response = {
            "cmd": "true",
            "args": "send_extension",
            "identifier": self.__identifier,
            "client_id": "APP",
            "destin": "EXTENSION",
            "bytecode": self.__bytecode
        }
        self.__ws.send(json.dumps(response))

    def __on_message(self, ws, mensagem):
        """
        Callback executado ao receber uma mensagem do servidor.

        Args:
            ws: Instância do WebSocket.
            mensagem (str): Mensagem recebida do servidor.
        """
        self.__mensagem = mensagem  # Armazena a mensagem recebida
        self.__ws.close()  # Fecha a conexão após o recebimento

    def __on_error(self, ws, erro):
        """
        Callback executado em caso de erro na conexão.

        Args:
            ws: Instância do WebSocket.
            erro (str): Detalhes do erro ocorrido.

        Raises:
            Exception: Exceção contendo a descrição do erro.
        """
        raise Exception(
            f"Erro: {erro}")

    def __on_close(self, ws, close_status_code, close_msg):
        """
        Callback executado quando a conexão WebSocket é encerrada.

        Args:
            ws: Instância do WebSocket.
            close_status_code: Código de encerramento.
            close_msg: Mensagem de encerramento.
        """
        pass  # Nada é executado durante o encerramento

    def start(self):
        """
        Inicia a conexão WebSocket e aguarda respostas.

        Raises:
            RuntimeWarning: Caso o BotGuardWs não tenha sido iniciado corretamente.
            Exception: Em caso de outros erros durante a execução.
        """
        try:
            if not self.__ws.sock or not self.__ws.sock.connected:
                # Inicia o WebSocket em uma thread separada
                ws_thread = threading.Thread(target=self.__ws.run_forever)
                ws_thread.start()
        except AttributeError:
            raise RuntimeWarning(
                "Certifique-se de ter inicializado o BotGuardWs corretamente!"
            )
        except Exception as e:
            raise Exception(
                f"Erro inesperado: {e}")

    def get_message(self) -> dict:
        """
        Retorna a mensagem recebida convertida para JSON.

        Returns:
            dict: Mensagem convertida em dicionário JSON.

        Raises:
            Exception: Caso não seja possível obter uma resposta do servidor.
            ValueError: Caso a mensagem recebida não seja um JSON válido.
        """
        try:
            if not self.__mensagem:
                raise Exception(
                    "Não foi possível obter uma resposta com o servidor!\n"
                    "\tCertifique-se de ter iniciado o BotGuardWs..."
                )
            return json.loads(self.__mensagem)
        except json.JSONDecodeError:
            raise ValueError(
                "Mensagem recebida não é um JSON válido.")
class BotGuardWs:
    def __init__(self):
        self.server = None  # O objeto de servidor será atribuído posteriormente

    async def __handle_client(self, websocket, path=None):
        """
        Processa as mensagens de um cliente conectado via WebSocket.
        """
        try:
            # Aguarda a primeira mensagem que identifica o cliente
            msg = await websocket.recv()
            try:
                msg_data = json.loads(msg)
            except json.JSONDecodeError:
                log = "Mensagem inválida, formato JSON esperado."
                log_message(log)
                await websocket.send(json.dumps({"error": log}))
                return

            client_id = msg_data.get('client_id')
            if client_id not in connected_clients_valid:
                log = "Identificador de cliente inválido."
                log_message(log)
                await websocket.send(json.dumps({"error": log}))
                return

            # Registra o cliente
            connected_clients[client_id] = websocket
            log_message(f"Cliente {client_id} conectado com sucesso.")

            # Processa os comandos enviados pelo cliente
            async for message in websocket:
                try:
                    msg_data = json.loads(message)
                except json.JSONDecodeError:
                    log = "Mensagem inválida, formato JSON esperado."
                    log_message(log)
                    await websocket.send(json.dumps({"error": log}))
                    continue

                cmd = msg_data.get('cmd')
                args = msg_data.get('args')
                destin = msg_data.get('destin')
                bot_guard_response = msg_data.get('bot_guard_response', '')
                po_token = msg_data.get('poToken', '')

                # Comando para enviar extensão: redireciona o bytecode para o cliente 'browser'
                if cmd == 'true' and args == 'send_extension' and client_id == 'APP':
                    bytecode = msg_data.get('bytecode', '')
                    identifier = msg_data.get('identifier', '')
                    response = {"cmd": "true", "args": bytecode, "identifier": identifier}
                    if 'browser' in connected_clients:
                        await connected_clients['browser'].send(json.dumps(response, ensure_ascii=False))
                        log_message("Comando enviado para o cliente 'browser'.")
                    else:
                        log_message("Cliente 'browser' não conectado.")

                # Processa respostas do BotGuard
                elif bot_guard_response:
                    if 'APP' in destin and 'APP' in connected_clients:
                        response = {"bot_guard_response": bot_guard_response, "po_token": po_token}
                        await connected_clients['APP'].send(json.dumps(response, ensure_ascii=False))
                    else:
                        log_message("Destino ou cliente APP não disponível.")
                else:
                    response = {"error": "Comando desconhecido"}
                    log = "Comando desconhecido recebido."
                    log_message(log)
                    await websocket.send(json.dumps(response, ensure_ascii=False))
        except websockets.exceptions.ConnectionClosed:
            log_message("Conexão fechada pelo cliente.")
        except KeyError as e:
            log = "Clientes ainda não estão todos conectados."
            log_message(log)
            await websocket.send(json.dumps({"error": log}, ensure_ascii=False))
        except Exception as e:
            log = f"Erro interno do servidor: {e}"
            log_message(log)
            raise Exception(log)
        finally:
            for cid, client_ws in list(connected_clients.items()):
                if client_ws == websocket:
                    del connected_clients[cid]
                    log_message(f"Cliente {cid} desconectado.")
                    break

    async def __main(self):
        """
        Inicia o servidor WebSocket e aguarda a finalização.
        """
        self.server = await websockets.serve(self.__handle_client, "127.0.0.1", 9090)
        await self.server.wait_closed()

    def __signal_handler(self, sig, frame):
        """
        Manipulador de sinal para encerrar o servidor.
        """
        if self.server:
            self.server.close()
            sys.exit()

    def __run_server(self):
        """
        Executa o servidor WebSocket utilizando um loop de eventos.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.__main())
        except Exception as e:
            log_message(f"Erro inesperado: {e}")
        finally:
            if self.server:
                loop.run_until_complete(self.server.wait_closed())
            loop.close()

    def start(self):
        """
        Inicia o servidor WebSocket em uma thread separada e configura os sinais.
        """
        print(f"{Fore.LIGHTMAGENTA_EX}\tBotGuardWs Online!{Style.RESET_ALL}")

        # Configura o manipulador de sinais para SIGINT
        signal.signal(signal.SIGINT, self.__signal_handler)
        # Registra SIGTSTP somente se estiver disponível (por exemplo, não disponível no Windows)
        if hasattr(signal, "SIGTSTP"):
            signal.signal(signal.SIGTSTP, self.__signal_handler)

        # Inicia o servidor em uma thread separada (daemon=True para permitir a finalização do programa)
        server_thread = threading.Thread(target=self.__run_server, daemon=True)
        server_thread.start()

        # Mantém a thread principal ativa para capturar os sinais
        try:
            while server_thread.is_alive():
                server_thread.join(timeout=1)
        except KeyboardInterrupt:
            ...
def start_ws():
    """
    Função principal que inicia o servidor WebSocket.
    """
    bot_guard_ws = BotGuardWs()
    bot_guard_ws.start()



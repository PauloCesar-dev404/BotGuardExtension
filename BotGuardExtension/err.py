class InvalidByteCode(Exception):
    """se o bytecode esta invalido..."""
    def __init__(self,msg:str):
        super().__init__(msg)
        self.mensagem = msg
# BotGuardExtension

![Versão](https://img.shields.io/badge/version-1.0.0.2-orange)
![Licença](https://img.shields.io/badge/license-MIT-orange)
[![Sponsor](https://img.shields.io/badge/💲Donate-yellow)](https://paulocesar-dev404.github.io/me-apoiando-online/)




é uma biblioteca que facilita a obtenção de atestações do **BotGuard** via WebSockets. Ela permite integrar seu navegador com a API do BotGuard, tornando a comunicação com o servidor mais eficiente e direta.

### Funcionalidades

- ✅ **PoToken**  
- ✅ **BotGuardResponse**  

---

## Iniciando

Antes de utilizar a extensão, é necessário iniciar o servidor WebSocket em seu ambiente virtual. Siga as instruções abaixo para configurar corretamente o ambiente.

### Instalação do Módulo

1. Acesse a [última versão disponível](https://github.com/PauloCesar-dev404/BotGuardExtension/releases/tag/latest).
2. Após baixar o arquivo `.whl` para o seu diretório local, instale-o via **pip**:

```bash
pip install "CAMINHO DO .whl BAIXADO"
```

---

## Como Usar

### 1. Iniciar o Servidor WebSocket

No seu ambiente virtual, execute o seguinte comando para iniciar o servidor WebSocket:

```bash
BG_Ws
```

Isso iniciará o servidor WebSocket em seu ambiente local. Agora, você pode criar seu cliente Python para conectar à extensão.

### 2. Criando o Cliente Python

Aqui está um exemplo simples de como obter um PoToken 


```python
from BotGuardExtension import BotGuardClient
bg_client = BotGuardClient()
program_byrecode = ''
video_id = ''
po_token = bg_client.get_bot_guard_reponse(program=program_byrecode,identifier=video_id)
print(po_token.get('po_token'))
```

---

## Extensão para o Navegador

Após baixar e descompactar o repositório, siga os passos abaixo para configurar a extensão no seu navegador.

### 1. Carregar a Extensão no Navegador

#### Microsoft Edge:

1. Acesse a página de extensões: `edge://extensions/`.
2. Ative a opção "Modo de desenvolvedor" no canto inferior esquerdo.
3. Clique em "Carregar sem compactação" e selecione a pasta `BotGuardBrowser` extraída do repositório.

#### Google Chrome:

1. Acesse a página de extensões: `chrome://extensions/`.
2. Ative a opção "Modo de desenvolvedor" no canto superior direito.
3. Clique em "Carregar sem compactação" e selecione a pasta `BotGuardBrowser`.

---

### 2. Iniciando o Cliente no Navegador

Após carregar a extensão, vá até o YouTube. Clique no ícone da extensão e ela criará um favorito que será o iniciador do seu cliente **Browser**. Esse favorito permitirá que você se conecte à API local do servidor WebSocket no seu ambiente.

![Favorito criado](assests/icon_fixed.png)

### 3. Como Usar

Agora, sempre que você quiser iniciar o cliente, basta clicar no favorito criado. Isso torna o processo simples e rápido!

---

## Considerações Finais

**BotGuardExtension** oferece uma maneira prática e eficiente de se comunicar com o servidor WebSocket local e integrar com a extensão do navegador. Siga os passos simples para configurar e começar a usar.


### Links Importantes:
- [Última Release](https://github.com/PauloCesar-dev404/BotGuardExtension/releases/tag/latest)
- [Apoie o projeto](https://paulocesar-dev404.github.io/me-apoiando-online/)

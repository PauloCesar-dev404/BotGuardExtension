const bookmarklet = `javascript:(function() {
  function createPopup(msg) {
      const overlay = document.createElement("div");
      overlay.style.position = "fixed";
      overlay.style.top = "0";
      overlay.style.left = "0";
      overlay.style.width = "100%";
      overlay.style.height = "100%";
      overlay.style.backgroundColor = "rgba(0, 0, 0, 0.6)";
      overlay.style.display = "flex";
      overlay.style.justifyContent = "center";
      overlay.style.alignItems = "center";
      overlay.style.zIndex = "1000";

      const popup = document.createElement("div");
      popup.style.backgroundColor = "white";
      popup.style.padding = "20px";
      popup.style.borderRadius = "10px";
      popup.style.boxShadow = "0 5px 15px rgba(0, 0, 0, 0.3)";
      popup.style.textAlign = "center";
      popup.style.width = "300px";

      const title = document.createElement("h2");
      title.textContent = "Aviso";
      popup.appendChild(title);

      const message = document.createElement("p");
      message.textContent = msg;
      message.style.color = '#1c3518eb';
      popup.appendChild(message);

      const closeButton = document.createElement("button");
      closeButton.textContent = "Fechar";
      closeButton.style.backgroundColor = "#007BFF";
      closeButton.style.color = "white";
      closeButton.style.border = "none";
      closeButton.style.padding = "10px 20px";
      closeButton.style.borderRadius = "5px";
      closeButton.style.cursor = "pointer";
      closeButton.style.fontSize = "14px";

      closeButton.addEventListener("click", function() {
          document.body.removeChild(overlay);
      });

      popup.appendChild(closeButton);
      overlay.appendChild(popup);
      document.body.appendChild(overlay);

      setTimeout(() => {
          if (document.body.contains(overlay)) {
              document.body.removeChild(overlay);
          }
      }, 3000);
  };

  function start_websocket() {
      let socket;
      const vm = window.trayride;
      const validDomains = ["youtube.com", "studio.youtube.com", "music.youtube.com", "kids.youtube.com"];

      if (!vm) {
          createPopup("Não foi possível carregar a vm!");
          return;
      };
      if (!vm.a) {
          createPopup("Não foi possível iniciar corretamente a máquina virtual do BG!");
          return;
      };
      if (socket && socket.readyState === WebSocket.OPEN) {
          createPopup("Você já está conectado ao WebSocket!");
          return;
      };

      function connectWebSocket() {
          try {
              socket = new WebSocket("ws://localhost:9090");

              socket.onopen = function() {
                  console.log("Conectado ao servidor WebSocket");
              };

              socket.onmessage = async function(message) {
                  try {
                      const msg = JSON.parse(message.data);
                      if (msg.cmd) {
                          console.log("Executando botGuard...");
                          await execute_program(msg.args, msg.identifier);
                      }
                  } catch (error) {
                      console.error("Erro ao processar mensagem do WebSocket:", error);
                  }
              };

              socket.onerror = function(error) {
                  console.error("Erro WebSocket:", error);
              };

              socket.onclose = function() {
                  console.log("Conexão WebSocket fechada");
              };

          } catch (error) {
              console.error("Erro ao conectar ao WebSocket:", error);
          }
      };

      function ping() {
          console.log("PING...");
          if (socket && socket.readyState === WebSocket.OPEN) {
              const jsonMessage = JSON.stringify({
                  bot_guard_response: "....",
                  args: "send_extension",
                  client_id: "browser",
                  destin: "APP",
              });
              socket.send(jsonMessage);
          } else {
              createPopup("WebSocket não está conectado.");
          }
      };

      function base64ToU8(base64) {
          const base64urlCharRegex = /[-_.]/g;
          const base64urlToBase64Map = {
              '-': '+',
              _: '/',
              '.': '='
            };
          let base64Mod;
        
          if (base64urlCharRegex.test(base64)) {
            base64Mod = base64.replace(base64urlCharRegex, function (match) {
              return base64urlToBase64Map[match];
            });
          } else {
            base64Mod = base64;
          }
        
          base64Mod = atob(base64Mod);
        
          return new Uint8Array([...base64Mod].map((char) => char.charCodeAt(0)));
        }
        function u8ToBase64(u8, base64url = false) {
          const result = btoa(String.fromCharCode(...u8));
        
          if (base64url) {
            return result.replace(/\\+/g, '-').replace(/\\//g, '_');
          }
        
          return result;
        }

      async function gerarSnapshot(args) {
          return new Promise((resolve, reject) => {
              if (!window.funcoesVM || !window.funcoesVM.funcaoSnapshotAssincrona) {
                  return reject(new Error("Função de snapshot assíncrona não encontrada"));
              }
              window.funcoesVM.funcaoSnapshotAssincrona(resposta => resolve(resposta), [
                  args.bindingConteudo,
                  args.timestampAssinado,
                  args.saidaSinalWebPo,
                  args.pularBufferPrivacidade,
              ]);
          });
      };

      async function getPoIntegrityToken(requestKey, botguardResponse) {
          const payload = [requestKey, botguardResponse];
          const integrityTokenResponse = await fetch('https://jnn-pa.googleapis.com/$rpc/google.internal.waa.v1.Waa/GenerateIT', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json+protobuf',
                  'x-goog-api-key': 'AIzaSyDyT5W0Jh49F30Pqqtyfdf7pDLFKLJoAnw',
                  'x-user-agent': 'grpc-web-javascript/0.1',
              },
              body: JSON.stringify(payload)
          });

          const integrityTokenJson = await integrityTokenResponse.json();
          const [integrityToken, estimatedTtlSecs, mintRefreshThreshold, websafeFallbackToken] = integrityTokenJson;

          return { integrityToken, estimatedTtlSecs, mintRefreshThreshold, websafeFallbackToken };
      };

      async function generatePoToken(getMinter, integrityTokenResponse) {
          if (!getMinter) throw new Error('PMD:Undefined');
          const mintCallback = await getMinter(base64ToU8(integrityTokenResponse.integrityToken ?? ''));
          if (!(mintCallback instanceof Function)) throw new Error('APF:Failed');
          const result = await mintCallback(new TextEncoder().encode("identifier"));
          if (!result) throw new Error('YNJ:Undefined');
          if (!(result instanceof Uint8Array)) throw new Error('ODM:Invalid');
          return u8ToBase64(result, true);
      };

      async function execute_program(programaBytecode, generate_poToken) {
          try {
              const callbackFuncoesVM = (funcaoSnapshotAssincrona, funcaoEncerrar, funcaoPassarEvento, funcaoVerificarCamera) => {
                  window.funcoesVM = { funcaoSnapshotAssincrona, funcaoEncerrar, funcaoPassarEvento, funcaoVerificarCamera };
              };

              const [funcaoSnapshotSincrona] = await vm.a(programaBytecode, callbackFuncoesVM, true, undefined, () => {}, [[], []]);

              const saidaSinalWebPo = [];
              const botguardResponse = await gerarSnapshot({ saidaSinalWebPo });
              const integrityTokenResponse = await getPoIntegrityToken('O43z0dpjhgX20SCx4KAo', botguardResponse);
              const getMinter = saidaSinalWebPo[0];

              let poToken;
              if (generate_poToken) {
                  poToken = await generatePoToken(getMinter, integrityTokenResponse);
              }

              setTimeout(() => {
                  if (socket && socket.readyState === WebSocket.OPEN) {
                      socket.send(JSON.stringify({
                          bot_guard_response: botguardResponse,
                          poToken: poToken,
                          args: "send_extension",
                          client_id: "browser",
                          destin: "APP",
                      }));
                  }
              }, 500);

          } catch (error) {
              createPopup("Erro ao executar o bytecode:", error);
          }
      };

      if (!validDomains.some(domain => window.location.hostname.endsWith(domain))) {
          createPopup("Você deve estar em uma página do YouTube, YouTube Studio, YouTube Music ou YouTube Kids!");
      } else {
          connectWebSocket();
          setTimeout(ping, 1000);
      }
  }

  start_websocket();
})();
`;


function criarFavoritoNaBarra(titulo, url) {
  if (!titulo || !url) {
    console.error("Título ou URL não fornecido.");
    return;
  }
  const barraDeFavoritosId = "1";
  chrome.bookmarks.search({}, (resultados) => {
    const duplicata = resultados.find((bookmark) =>
      (bookmark.parentId === barraDeFavoritosId && bookmark.title === titulo) ||
      (bookmark.parentId === barraDeFavoritosId && bookmark.url === url)
    );
    if (duplicata) {
      return;
    }
    chrome.bookmarks.create({ parentId: barraDeFavoritosId, title: titulo, url: url }, (novoFavorito) => {
      if (chrome.runtime.lastError) {
        console.error("Erro ao criar o favorito na barra de favoritos:", chrome.runtime.lastError.message);
        return;
      }
      console.log(`Favorito criado com sucesso na barra de favoritos!`);
    });
  });
};
chrome.action.onClicked.addListener(() => {
  criarFavoritoNaBarra("🗿 Start botGuard", bookmarklet);
});

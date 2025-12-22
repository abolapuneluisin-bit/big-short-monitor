import asyncio
import os
from playwright.async_api import async_playwright

# --- CONFIGURAÇÕES ---
# Identificado automaticamente como 'rejao'
USUARIO_MAC = "rejao" 
CAMINHO_CHROME = f"/Users/{USUARIO_MAC}/Library/Application Support/Google/Chrome"

class LuisinSuperAgente:
    def __init__(self):
        self.browser_context = None
        self.page = None

    async def iniciar_sessao(self):
        print("🚀 Iniciando o Cérebro do Luisin...")
        try:
            async with async_playwright() as p:
                # Inicia o Chrome com o seu PERFIL REAL (Luisin A Bola Pune)
                # Isso garante que você já esteja logado no Google, Zap, etc.
                print(f"📂 Usando perfil de: {CAMINHO_CHROME}")
                
                self.browser_context = await p.chromium.launch_persistent_context(
                    user_data_dir=CAMINHO_CHROME,
                    channel="chrome",  # Usa o Chrome instalado no Mac
                    headless=False,    # False para você ver o robô trabalhando
                    args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
                )
                
                self.page = self.browser_context.pages[0]
                
                # --- TAREFA 1: HEYGEN (Criação de Conta/Login) ---
                try:
                    await self.acessar_heygen()
                except Exception as e:
                    print(f"⚠️ Erro ao acessar HeyGen: {e}")

                # --- TAREFA 2: MONITORAR WHATSAPP (Áudio) ---
                try:
                    await self.monitorar_whatsapp()
                except Exception as e:
                    print(f"⚠️ Erro ao monitorar WhatsApp: {e}")

                # Mantém o robô rodando
                print("🤖 Robô ativo. Pressione Ctrl+C no terminal para encerrar.")
                await asyncio.Future() 

        except Exception as e:
            print(f"\n❌ ERRO CRÍTICO: {e}")
            if "SingletonLock" in str(e):
                print("⚠️ PARECE QUE O CHROME JÁ ESTÁ ABERTO.")
                print("💡 Solução: Feche TOTALMENTE o Google Chrome (Command+Q) e tente novamente.")

    async def acessar_heygen(self):
        print("🎥 Acessando HeyGen...")
        await self.page.goto("https://app.heygen.com/login")
        await self.page.wait_for_timeout(3000)

        # Tenta clicar no botão "Sign in with Google" se estiver visível
        # O seletor pode mudar, mas geralmente contém texto relacionado ao Google
        # Usando seletores mais genéricos para garantir robustez
        botao_google = self.page.get_by_role("button", name="Google").first
        if not await botao_google.is_visible():
             botao_google = self.page.get_by_text("Sign in with Google", exact=False).first

        if await botao_google.is_visible():
            print("🔵 Botão Google detectado. Tentando login automático...")
            await botao_google.click()
            # Como o perfil já está logado no Chrome, ele deve passar direto 
            # ou pedir apenas um clique de confirmação.
            print("✅ Clique realizado. Verifique se o login ocorreu.")
        else:
            print("ℹ️ Parece que já estamos logados no HeyGen (ou o botão não foi encontrado).")

        # Aqui você adicionaria a lógica para clicar em "API" e gerar a chave
        # await self.page.goto("https://app.heygen.com/settings/api")
            

    async def monitorar_whatsapp(self):
        print("🟢 Abrindo WhatsApp Web e escutando áudios...")
        page_zap = await self.browser_context.new_page()
        await page_zap.goto("https://web.whatsapp.com/")

        # Define o que fazer quando um arquivo de áudio passar pela rede
        async def interceptar_audio(response):
            # O WhatsApp usa formatos como ogg ou m4a para áudios
            content_type = response.headers.get("content-type", "")
            if "audio" in content_type or "ogg" in response.url:
                print(f"🎤 Áudio detectado! URL: {response.url[:50]}...")
                
                # Cria uma pasta para salvar os áudios
                if not os.path.exists("audios_recebidos"):
                    os.makedirs("audios_recebidos")
                
                # Gera um nome único
                import time
                timestamp = int(time.time() * 1000)
                extensao = "ogg"
                if "mp4" in content_type: extensao = "m4a"
                if "mpeg" in content_type: extensao = "mp3"

                nome_arquivo = f"audios_recebidos/audio_{timestamp}.{extensao}"
                
                try:
                    # Salva o áudio no disco
                    body = await response.body()
                    with open(nome_arquivo, "wb") as f:
                        f.write(body)
                    
                    print(f"💾 Áudio salvo em: {nome_arquivo}")
                    print("🤖 (Aqui o Agente enviaria para a transcrição no OpenAI/Gemini...)")
                except Exception as ex:
                    print(f"Erro ao salvar áudio: {ex}")

        # Ativa o "escuta" de rede
        page_zap.on("response", interceptar_audio)

        print("👂 Agente Luisin está ouvindo o WhatsApp. Mande um áudio para testar!")

# Executa o Agente
if __name__ == "__main__":
    agente = LuisinSuperAgente()
    asyncio.run(agente.iniciar_sessao())

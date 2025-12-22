import asyncio
import re
import os
from playwright.async_api import async_playwright

# ==============================================================================
# ⚙️ CONFIGURAÇÕES DO AGENTE LUISIN
# ==============================================================================

# ⚠️ CONFIGURAÇÃO AUTOMÁTICA: Pegou seu usuário do Mac sozinho!
USUARIO_MAC = os.getenv("USER")

# Caminho do Perfil do Chrome no macOS
DIRETORIO_DADOS = f"/Users/{USUARIO_MAC}/Library/Application Support/Google/Chrome"

# ==============================================================================
# 🧠 CÉREBRO DO AGENTE
# ==============================================================================

class LuisinSuperAgente:
    def __init__(self):
        self.browser_context = None
        self.page = None

    async def iniciar(self):
        print("\n🤖 === INICIANDO SUPER AGENTE LUISIN === 🤖")
        print(f"📂 Usando perfil do Chrome de: {USUARIO_MAC}")
        print(f"📂 Caminho: {DIRETORIO_DADOS}")
        print("⚠️  Certifique-se de que o Chrome está FECHADO antes de continuar.\n")

        async with async_playwright() as p:
            try:
                # Inicia o Chrome com o seu PERFIL REAL (Cookies, Senhas, Zap Logado)
                self.browser_context = await p.chromium.launch_persistent_context(
                    user_data_dir=DIRETORIO_DADOS,
                    channel="chrome",      # Usa o Chrome instalado
                    headless=False,        # Mostra o navegador (True para esconder)
                    args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
                )
                
                # Pega a primeira aba aberta
                self.page = self.browser_context.pages[0]
                
                # --- ORQUESTRAÇÃO DE TAREFAS ---
                
                # 1. TAREFA: Verificar se precisamos de código no Gmail (Exemplo)
                # await self.buscar_codigo_gmail() 
                
                # 2. TAREFA: Tentar logar/acessar HeyGen
                await self.acessar_heygen()

                # 3. TAREFA: Monitorar WhatsApp (Fica rodando em loop)
                await self.monitorar_whatsapp()

                # Mantém o robô vivo indefinidamente
                print("⏳ Agente rodando e aguardando comandos/áudios...")
                await asyncio.Future()

            except Exception as e:
                print(f"❌ ERRO CRÍTICO: {e}")
                print("DICA: Verifique se o Chrome estava realmente fechado.")

    # --------------------------------------------------------------------------
    # 🛠️ FUNÇÃO 1: RESGATAR CÓDIGO NO GMAIL
    # --------------------------------------------------------------------------
    async def buscar_codigo_gmail(self):
        print("📧 Acessando Gmail para buscar códigos de verificação...")
        try:
            # Abre nova aba para não atrapalhar a principal
            page_mail = await self.browser_context.new_page()
            await page_mail.goto("https://mail.google.com/mail/u/0/#inbox")
            
            # Espera carregar a lista
            await page_mail.wait_for_selector('tr.zA', state="visible")
            
            # Pega o e-mail mais recente
            email_recente = page_mail.locator('tr.zA').first
            assunto = await email_recente.inner_text()
            print(f"📨 Lendo último e-mail: {assunto[:40]}...")
            
            await email_recente.click()
            await page_mail.wait_for_timeout(2000)
            
            # Extrai o corpo do e-mail
            corpo_email = await page_mail.locator("div.a3s.aiL").first.inner_text()
            
            # Procura números de 4 a 6 dígitos
            match = re.search(r'\b\d{4,6}\b', corpo_email)
            
            if match:
                codigo = match.group(0)
                print(f"✅ CÓDIGO ENCONTRADO: {codigo}")
                await page_mail.close()
                return codigo
            else:
                print("⚠️ Nenhum código óbvio encontrado.")
                await page_mail.close()
                return None
        except Exception as e:
            print(f"⚠️ Erro ao ler Gmail: {e}")

    # --------------------------------------------------------------------------
    # 🛠️ FUNÇÃO 2: ACESSAR HEYGEN (VÍDEO)
    # --------------------------------------------------------------------------
    async def acessar_heygen(self):
        print("🎥 Verificando acesso ao HeyGen...")
        try:
            # Usa a aba principal
            await self.page.goto("https://app.heygen.com/login")
            await self.page.wait_for_timeout(3000)
            
            # Tenta identificar botão de login Google
            # Usando seletores robustos
            botao_google = self.page.get_by_text("Google", exact=False).first
            if not await botao_google.is_visible():
                 botao_google = self.page.get_by_role("button", name="Google").first
            
            if await botao_google.is_visible():
                print("🔵 Botão Google detectado. Clicando...")
                await botao_google.click()
            else:
                print("ℹ️ Provavelmente já estamos logados.")
        except Exception as e:
            print(f"⚠️ Erro no HeyGen: {e}")

    # --------------------------------------------------------------------------
    # 🛠️ FUNÇÃO 3: MONITORAR WHATSAPP (ÁUDIO/VENDAS)
    # --------------------------------------------------------------------------
    async def monitorar_whatsapp(self):
        print("🟢 Iniciando Monitoramento do WhatsApp Web (37 9 84120360)...")
        
        page_zap = await self.browser_context.new_page()
        await page_zap.goto("https://web.whatsapp.com/")
        
        # Garante que a pasta de audios existe
        if not os.path.exists("audios_recebidos"):
            os.makedirs("audios_recebidos")

        # Função interna que roda toda vez que passar um arquivo pela rede
        async def interceptar_audio(response):
            try:
                # Filtra apenas arquivos de áudio (mensagens de voz costumam ser ogg/opus)
                if "audio" in response.headers.get("content-type", ""):
                    url = response.url
                    # Ignora sons de notificação do próprio whatsapp
                    if "dyn" in url or "pps" in url: 
                        return

                    print(f"🎤 Áudio de cliente detectado!")
                    
                    # Nome único baseado no tempo
                    import time
                    nome_arquivo = f"audios_recebidos/audio_{int(time.time() * 1000)}.ogg"
                    
                    # Salva o arquivo
                    with open(nome_arquivo, "wb") as f:
                        f.write(await response.body())
                    
                    print(f"💾 Salvo em: {nome_arquivo}")
                    print("🤖 (AQUI ENTRARIA O PROMPT DE VENDAS PARA RESPONDER O CLIENTE...)")
                    
            except Exception as e:
                pass # Ignora erros de rede irrelevantes

        # Ativa o "escuta"
        page_zap.on("response", interceptar_audio)
        print("👂 Agente ouvindo... Pode mandar áudio no Zap!")

# ==============================================================================
# 🚀 EXECUÇÃO
# ==============================================================================
if __name__ == "__main__":
    agente = LuisinSuperAgente()
    asyncio.run(agente.iniciar())

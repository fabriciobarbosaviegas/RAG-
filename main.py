import logging
from pathlib import Path
from src.ragsystem import RAGSystem

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rag_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """
    Função principal - PERSONALIZE AQUI!
    Adicione seus PDFs, sites e faça suas perguntas
    """

    print("="*70)
    print("🚀 SISTEMA RAG - 100% OPEN SOURCE (Ollama + Llama)")
    print("="*70)

    try:
        # ========================================
        # PASSO 1: Inicializa o sistema
        # ========================================
        rag = RAGSystem(model_name="llama3.2:3b")

        # ========================================
        # PASSO 2: ADICIONE SEUS PDFs AQUI ⬇️
        # ========================================
        print("\n📂 Adicionando documentos PDF...")

        # IMPORTANTE: Use caminhos compatíveis com Windows/Linux/Mac
        # Opção 1: Caminho relativo (recomendado)
        # rag.add_document(str(Path("data") / "RAG-2021.pdf"))
        # rag.add_document(str(Path("data") / "plano_municipal_saude.pdf"))
        
        # Opção 2: Caminho absoluto Windows
        # rag.add_document(r"C:\Users\SeuNome\Documents\RAG-2021.pdf")
        
        # Opção 3: Caminho absoluto usando pathlib (multiplataforma)
        # rag.add_document(str(Path.home() / "Downloads" / "RAG-2021.pdf"))
        
        # Exemplo: Arquivos TXT e DOCX também funcionam
        # rag.add_document(str(Path("data") / "arquivo.txt"))
        # rag.add_document(str(Path("data") / "artigo.docx"))

        # Exemplo: Lista de PDFs em loop
        # pdfs = [
        #     str(Path("data") / "pdf1.pdf"),
        #     str(Path("data") / "pdf2.pdf"),
        #     str(Path("data") / "pdf3.pdf")
        # ]
        # for pdf in pdfs:
        #     rag.add_document(pdf)
        
        # ⚠️ COMENTADO: Descomente e ajuste os caminhos acima para seus arquivos reais
        print("⚠️  Nenhum documento adicionado. Descomente os exemplos acima e ajuste os caminhos.")

        # ========================================
        # PASSO 3: ADICIONE SEUS SITES AQUI ⬇️
        # ========================================
        print("\n🌐 Adicionando sites...")

        # Exemplo 1: Site único
        # rag.add_url("https://ucpel.edu.br/servicos/unidades-basicas-de-saude")

        # Exemplo 2: Lista de URLs em loop
        # urls = [
        #     "https://site1.com/artigo",
        #     "https://site2.com/noticia",
        #     "https://site3.com/pesquisa"
        # ]
        # for url in urls:
        #     rag.add_url(url)
        
        # ⚠️ COMENTADO: Descomente e ajuste as URLs acima para seus sites reais
        print("⚠️  Nenhuma URL adicionada. Descomente os exemplos acima e ajuste as URLs.")

        # ========================================
        # PASSO 4: Constrói o índice (OBRIGATÓRIO!)
        # ========================================
        rag.build_vectorstore()

        # Modo interativo com memória
        print("\n💡 Modo interativo COM MEMÓRIA INTELIGENTE ativado!")
        print("Comandos especiais:")
        print("  - 'memoria' ou 'historico': Mostra histórico")
        print("  - 'limpar': Limpa memória manualmente")
        print("  - 'auto on': Ativa limpeza automática ao mudar de assunto")
        print("  - 'auto off': Desativa limpeza automática")
        print("  - 'sair': Encerra\n")

        auto_clear = True  # Ativa limpeza automática por padrão
        print("🔄 Limpeza automática de contexto: ATIVADA\n")

        while True:
            pergunta = input("\n❓ Sua pergunta: ")

            if pergunta.lower() in ['sair', 'exit', 'quit']:
                print("👋 Encerrando...")
                break

            if pergunta.lower() in ['memoria', 'histórico', 'historico', 'memory']:
                rag.show_memory()
                continue

            if pergunta.lower() in ['limpar', 'clear', 'reset']:
                rag.clear_memory()
                continue

            if pergunta.lower() == 'auto on':
                auto_clear = True
                print("✅ Limpeza automática ATIVADA")
                continue

            if pergunta.lower() == 'auto off':
                auto_clear = False
                print("❌ Limpeza automática DESATIVADA")
                continue

            resposta = rag.query(pergunta, show_context=False, auto_clear_memory=auto_clear)
            print(f"\n📝 Resposta:\n{resposta}")

    except FileNotFoundError as e:
        logger.error(f"Arquivo não encontrado: {e}")
        print(f"\n❌ Erro: {str(e)}")
        print("\n🔧 Dica: Verifique se o caminho do arquivo está correto e se o arquivo existe.")
    except ConnectionError as e:
        logger.error(f"Erro de conexão: {e}")
        print(f"\n❌ Erro de Conexão: {str(e)}")
        print("\n🔧 Dica: Verifique sua conexão com a internet ou se a URL está acessível.")
    except ValueError as e:
        logger.error(f"Erro de validação: {e}")
        print(f"\n❌ Erro: {str(e)}")
    except Exception as e:
        logger.exception("Erro inesperado no sistema RAG")
        print(f"\n❌ Erro: {str(e)}")
        print("\n🔧 Dicas:")
        print("1. Verifique se os caminhos dos arquivos estão corretos")
        print("2. Confirme que o Ollama está rodando")
        print("   - Windows: Execute 'ollama serve' em um terminal")
        print("   - Teste com: 'ollama list'")
        print("3. Verifique o arquivo de log 'rag_system.log' para mais detalhes")

if __name__ == "__main__":
    main()

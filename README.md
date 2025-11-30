# RAG System - Sistema Refinado

✅ **Status**: O sistema foi refinado e está pronto para uso!

## 📋 Pré-requisitos

1. **Python 3.8+** instalado
2. **Ollama** instalado e rodando
   - Windows: Baixe do [ollama.com](https://ollama.com)  
   - Execute `ollama serve` em um terminal

## 🚀 Instalação

```powershell
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Verificar Ollama
ollama list

# 3. Se o modelo llama3.2:3b não estiver instalado:
ollama pull llama3.2:3b
```

## 📂 Estrutura do Projeto

```
rag/
├── main.py              # Arquivo principal de execução
├── src/
│   ├── __init__.py      # Torna src um pacote Python
│   ├── config.py        # Configurações do sistema
│   ├── memory.py        # Gestão de histórico de conversa
│   ├── loaders.py       # Carregamento de PDF, DOCX e Web Scraping
│   ├── proccessing.py   # Chunking de texto
│   ├── llm.py           # Gerenciador do Ollama
│   └── ragsystem.py     # Orquestrador principal
├── requirements.txt     # Dependências Python
└── rag_system.log      # Log de execução (criado automaticamente)
```

## ⚙️ Configuração

Edite `main.py` para adicionar seus documentos:

```python
# Adicionar PDFs (caminhos relativos ou absolutos)
rag.add_document(str(Path("data") / "seu_arquivo.pdf"))
rag.add_document(r"C:\Users\SeuNome\Documents\outro_arquivo.pdf")

# Adicionar URLs
rag.add_url("https://example.com/artigo")

# Construir índice (obrigatório!)
rag.build_vectorstore()
```

## 🏃 Uso

```powershell
python main.py
```

### Comandos Disponíveis

Durante a

 execução interativa:
- `memoria` / `historico` - Mostra o histórico da conversa
- `limpar` / `clear` - Limpa o histórico manualmente
- `auto on` - Ativa limpeza automática ao mudar de assunto
- `auto off` - Desativa limpeza automática
- `sair` / `exit` - Encerra o programa

## 🔍 Debugging

Se algo der errado, verifique:

1. **Arquivo de Log**: `rag_system.log` contém detalhes de todas as operações
2. **Ollama**: Certifique-se que está rodando (`ollama list`)
3. **Caminhos**: Use caminhos absolutos ou relativos corretos

## 🛠️ Melhorias Implementadas

✅ **Imports Corrigidos** - Sistema modular com `src` como pacote Python  
✅ **Logging Completo** - Logs detalhados em todos os módulos  
✅ **Caminhos  Multiplataforma** - Uso de `pathlib` em todo o sistema  
✅ **Tratamento de Erros Robusto** - Mensagens claras e logs informativos  
✅ **Compatibilidade Windows/Linux/Mac** - Paths agnósticos ao SO  

## 📝 Notas Técnicas

- **Modelo de Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (local, sem custo)
- **Vector Store**: ChromaDB com persistência em`./chroma_db`
- **Chunking**: 1200 caracteres com overlap de 300
- **Memória Conversacional**: Últimos 3 turnos (configurável)

## 🐛 Troubleshooting

| Erro | Solução |
|------|---------|
| `ModuleNotFoundError: langchain_community` | Execute `pip install -r requirements.txt` |
| `Ollama não está rodando` | Execute `ollama serve` em um terminal |
| `Arquivo não encontrado` | Verifique os caminhos em `main.py` |
| `URL timeout` | Verifique sua conexão e se a URL é acessível |
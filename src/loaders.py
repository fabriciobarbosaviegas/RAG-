import logging
from pathlib import Path
import pypdf
import requests
from bs4 import BeautifulSoup
from docx import Document as DocxDocument

# Configurar logger
logger = logging.getLogger(__name__)

class DocumentLoader:
    """Carrega e processa diferentes tipos de documentos"""

    @staticmethod
    def load_txt(file_path: str) -> str:
        """Carrega arquivo de texto simples"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Tenta com outra codificação se UTF-8 falhar
            logger.warning(f"Falha ao ler {file_path} com UTF-8, tentando latin-1...")
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Erro ao carregar {file_path} com latin-1: {e}")
                raise Exception(f"Erro ao carregar arquivo TXT '{Path(file_path).name}': Problema com codificação do arquivo")
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {file_path}")
            raise FileNotFoundError(f"Arquivo TXT não encontrado: {file_path}")
        except Exception as e:
            logger.error(f"Erro inesperado ao carregar {file_path}: {e}")
            raise Exception(f"Erro ao carregar arquivo TXT '{Path(file_path).name}': {str(e)}")

    @staticmethod
    def load_pdf(file_path: str) -> str:
        """Carrega e extrai texto de arquivo PDF"""
        try:
            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = pypdf.PdfReader(f)
                num_pages = len(pdf_reader.pages)
                logger.info(f"Extraindo texto de {num_pages} páginas do PDF...")
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            if not text.strip():
                logger.warning(f"PDF {Path(file_path).name} não contém texto extraível")
                raise ValueError(f"O PDF '{Path(file_path).name}' parece estar vazio ou ser somente imagem")
            
            return text
        except FileNotFoundError:
            logger.error(f"Arquivo PDF não encontrado: {file_path}")
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {file_path}")
        except pypdf.errors.PdfReadError as e:
            logger.error(f"Erro ao ler PDF {file_path}: {e}")
            raise Exception(f"Erro ao ler PDF '{Path(file_path).name}': Arquivo pode estar corrompido ou protegido")
        except Exception as e:
            logger.error(f"Erro inesperado ao processar PDF {file_path}: {e}")
            raise Exception(f"Erro ao carregar PDF '{Path(file_path).name}': {str(e)}")

    @staticmethod
    def load_docx(file_path: str) -> str:
        """Carrega e extrai texto de arquivo DOCX"""
        try:
            doc = DocxDocument(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            if not text.strip():
                logger.warning(f"DOCX {Path(file_path).name} não contém texto")
                raise ValueError(f"O arquivo DOCX '{Path(file_path).name}' está vazio")
            
            return text
        except FileNotFoundError:
            logger.error(f"Arquivo DOCX não encontrado: {file_path}")
            raise FileNotFoundError(f"Arquivo DOCX não encontrado: {file_path}")
        except Exception as e:
            logger.error(f"Erro ao carregar DOCX {file_path}: {e}")
            raise Exception(f"Erro ao carregar arquivo DOCX '{Path(file_path).name}': {str(e)}")

    @staticmethod
    def load_file(file_path: str) -> str:
        """Detecta tipo de arquivo e carrega apropriadamente"""
        path = Path(file_path)
        
        if not path.exists():
            logger.error(f"Arquivo não encontrado: {file_path}")
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        extension = path.suffix.lower()

        if extension == '.txt':
            return DocumentLoader.load_txt(file_path)
        elif extension == '.pdf':
            return DocumentLoader.load_pdf(file_path)
        elif extension == '.docx':
            return DocumentLoader.load_docx(file_path)
        else:
            logger.error(f"Tipo de arquivo não suportado: {extension}")
            raise ValueError(f"Tipo de arquivo não suportado: {extension}. Use .txt, .pdf ou .docx")
        
class WebScraper:
    """Realiza web scraping de URLs"""

    @staticmethod
    def scrape_url(url: str) -> str:
        """
        Extrai texto de uma URL

        Args:
            url: URL para fazer scraping

        Returns:
            Texto extraído da página
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            logger.info(f"Acessando URL: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove scripts e estilos
            for script in soup(["script", "style"]):
                script.decompose()

            # Extrai texto
            text = soup.get_text()

            # Limpa o texto
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            if not text.strip():
                logger.warning(f"URL {url} não retornou texto extraível")
                raise ValueError(f"A URL não contém texto extraível: {url}")

            logger.info(f"Texto extraído com sucesso da URL: {len(text)} caracteres")
            return text

        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao acessar {url}")
            raise Exception(f"Timeout: A URL demorou muito para responder (>10s): {url}")
        except requests.exceptions.ConnectionError:
            logger.error(f"Erro de conexão ao acessar {url}")
            raise Exception(f"Erro de conexão: Não foi possível conectar à URL: {url}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erro HTTP ao acessar {url}: {e}")
            raise Exception(f"Erro HTTP {e.response.status_code}: {url}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao acessar URL {url}: {e}")
            raise Exception(f"Erro ao acessar URL: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao processar {url}: {e}")
            raise Exception(f"Erro ao processar conteúdo da URL: {str(e)}")
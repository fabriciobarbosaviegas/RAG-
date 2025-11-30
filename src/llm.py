import logging
import ollama

# Configurar logger
logger = logging.getLogger(__name__)

class OllamaManager:
    """Gerencia interações com o servidor Ollama"""

    @staticmethod
    def check_ollama_running() -> bool:
        """Verifica se o servidor Ollama está rodando"""
        try:
            response = ollama.list()
            logger.info("Ollama está rodando e acessível")
            return True
        except Exception as e:
            logger.error(f"Ollama não está rodando ou não é acessível: {e}")
            return False

    @staticmethod
    def check_model_available(model_name: str) -> bool:
        """Verifica se um modelo está disponível localmente"""
        try:
            models = ollama.list()
            available = any(model_name in model['name'] for model in models.get('models', []))
            if available:
                logger.info(f"Modelo {model_name} encontrado localmente")
            else:
                logger.warning(f"Modelo {model_name} não encontrado localmente")
            return available
        except Exception as e:
            logger.error(f"Erro ao verificar disponibilidade do modelo: {e}")
            return False

    @staticmethod
    def pull_model(model_name: str):
        """Baixa um modelo do Ollama"""
        try:
            logger.info(f"Iniciando download do modelo {model_name}...")
            print(f"📥 Baixando modelo {model_name}... (isso pode levar alguns minutos)")
            ollama.pull(model_name)
            logger.info(f"Modelo {model_name} baixado com sucesso")
            print(f"✅ Modelo {model_name} baixado com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao baixar modelo {model_name}: {e}")
            raise Exception(f"Erro ao baixar modelo: {str(e)}")

    @staticmethod
    def generate_response(model: str, prompt: str, system_prompt: str = "",
                         temperature: float = 0.7) -> str:
        """
        Gera resposta usando Ollama

        Args:
            model: Nome do modelo
            prompt: Prompt do usuário
            system_prompt: Prompt do sistema
            temperature: Temperatura para geração

        Returns:
            Resposta gerada
        """
        try:
            logger.debug(f"Gerando resposta com modelo {model}, temperatura {temperature}")
            response = ollama.generate(
                model=model,
                prompt=prompt,
                system=system_prompt,
                options={'temperature': temperature}
            )
            logger.info(f"Resposta gerada com sucesso ({len(response['response'])} caracteres)")
            return response['response']
        except Exception as e:
            logger.error(f"Erro na geração de resposta: {e}")
            raise Exception(f"Erro na geração: {str(e)}")
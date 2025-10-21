"""
Configurações específicas para produção/hospedagem
"""
import os
from dotenv import load_dotenv

load_dotenv()

class ProductionSettings:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Server - Configurações para produção
    HOST = "0.0.0.0"
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = False
    
    # Diretórios - Usar diretórios temporários
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    TEMP_DIR = os.path.join(BASE_DIR, "temp")
    
    # Limites para hospedagem compartilhada
    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB (aumentado para PDFs grandes)
    MAX_REQUEST_SIZE = 50 * 1024 * 1024  # 50MB total
    
    # Timeouts
    REQUEST_TIMEOUT = 120  # 2 minutos
    AI_TIMEOUT = 60  # 1 minuto para IA
    
    # Configurações de segurança
    ALLOWED_EXTENSIONS = {
        'pdf': ['.pdf'],
        'presentation': ['.pptx', '.ppt'],
        'document': ['.docx', '.doc'],
        'image': ['.jpg', '.jpeg', '.png', '.gif']
    }
    
    # Configurações de IA
    AI_MODELS = {
        'openai': 'gpt-3.5-turbo',  # Modelo mais barato
        'anthropic': 'claude-3-haiku-20240307'  # Modelo mais barato
    }
    
    # Rate limiting
    MAX_REQUESTS_PER_MINUTE = 10
    MAX_AI_REQUESTS_PER_HOUR = 50

production_settings = ProductionSettings()

# Criar diretórios necessários
try:
    for directory in [production_settings.UPLOAD_DIR, 
                     production_settings.OUTPUT_DIR, 
                     production_settings.TEMP_DIR]:
        os.makedirs(directory, exist_ok=True)
except Exception as e:
    print(f"Aviso: Não foi possível criar diretório: {e}")

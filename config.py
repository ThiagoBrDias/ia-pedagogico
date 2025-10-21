import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Server - Adaptado para hospedagem
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Diretórios - Usar /tmp para hospedagem compartilhada
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    TEMP_DIR = os.path.join(BASE_DIR, "temp")
    
    # Limites para hospedagem compartilhada
    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB (aumentado para PDFs grandes)
    ALLOWED_EXTENSIONS = {
        'pdf': ['.pdf'],
        'presentation': ['.pptx', '.ppt'],
        'document': ['.docx', '.doc'],
        'image': ['.jpg', '.jpeg', '.png', '.gif']
    }

settings = Settings()

# Criar diretórios necessários (apenas se não existirem)
try:
    for directory in [settings.UPLOAD_DIR, settings.OUTPUT_DIR, settings.TEMP_DIR]:
        os.makedirs(directory, exist_ok=True)
except Exception as e:
    print(f"Aviso: Não foi possível criar diretório {directory}: {e}")


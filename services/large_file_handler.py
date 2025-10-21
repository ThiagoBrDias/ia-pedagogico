"""
Serviço para lidar com arquivos grandes
"""
import os
import tempfile
import shutil
from typing import Optional
import asyncio

class LargeFileHandler:
    def __init__(self, max_size: int = 25 * 1024 * 1024):
        self.max_size = max_size
        self.temp_dir = tempfile.gettempdir()
    
    async def save_large_file(self, file_content: bytes, filename: str) -> Optional[str]:
        """
        Salva arquivo grande em chunks para evitar timeout
        """
        try:
            if len(file_content) > self.max_size:
                return None
            
            # Criar arquivo temporário
            temp_path = os.path.join(self.temp_dir, f"temp_{filename}")
            
            # Salvar em chunks para não sobrecarregar a memória
            chunk_size = 1024 * 1024  # 1MB por chunk
            
            with open(temp_path, 'wb') as f:
                for i in range(0, len(file_content), chunk_size):
                    chunk = file_content[i:i + chunk_size]
                    f.write(chunk)
                    # Pequena pausa para não sobrecarregar
                    await asyncio.sleep(0.01)
            
            return temp_path
            
        except Exception as e:
            print(f"Erro ao salvar arquivo grande: {e}")
            return None
    
    def cleanup_temp_file(self, file_path: str):
        """
        Remove arquivo temporário
        """
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Erro ao limpar arquivo temporário: {e}")
    
    def get_file_info(self, file_path: str) -> dict:
        """
        Obtém informações do arquivo
        """
        try:
            stat = os.stat(file_path)
            return {
                "size": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "readable": True
            }
        except Exception as e:
            return {
                "size": 0,
                "size_mb": 0,
                "readable": False,
                "error": str(e)
            }
    
    def split_large_pdf(self, file_path: str, max_pages: int = 50) -> list:
        """
        Divide PDF grande em partes menores
        """
        try:
            from PyPDF2 import PdfReader, PdfWriter
            
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            
            if total_pages <= max_pages:
                return [file_path]
            
            # Dividir em chunks
            chunks = []
            for start in range(0, total_pages, max_pages):
                end = min(start + max_pages, total_pages)
                
                writer = PdfWriter()
                for page_num in range(start, end):
                    writer.add_page(reader.pages[page_num])
                
                chunk_path = os.path.join(
                    self.temp_dir, 
                    f"chunk_{start}_{end}_{os.path.basename(file_path)}"
                )
                
                with open(chunk_path, 'wb') as output_file:
                    writer.write(output_file)
                
                chunks.append(chunk_path)
            
            return chunks
            
        except Exception as e:
            print(f"Erro ao dividir PDF: {e}")
            return [file_path]
    
    def compress_pdf(self, file_path: str) -> Optional[str]:
        """
        Comprime PDF para reduzir tamanho
        """
        try:
            from PyPDF2 import PdfReader, PdfWriter
            
            reader = PdfReader(file_path)
            writer = PdfWriter()
            
            # Adicionar todas as páginas
            for page in reader.pages:
                # Comprimir página
                page.compress_content_streams()
                writer.add_page(page)
            
            # Salvar versão comprimida
            compressed_path = os.path.join(
                self.temp_dir,
                f"compressed_{os.path.basename(file_path)}"
            )
            
            with open(compressed_path, 'wb') as output_file:
                writer.write(output_file)
            
            return compressed_path
            
        except Exception as e:
            print(f"Erro ao comprimir PDF: {e}")
            return None

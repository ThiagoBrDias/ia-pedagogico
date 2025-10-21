import os
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color
import io

class PDFService:
    def extract_text(self, file_path: str) -> str:
        """Extrair texto de um PDF"""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Erro ao extrair texto do PDF: {str(e)}")
    
    def merge_pdfs(self, file_paths: list, output_dir: str) -> str:
        """Mesclar múltiplos PDFs"""
        try:
            merger = PdfMerger()
            for pdf in file_paths:
                merger.append(pdf)
            
            output_path = os.path.join(output_dir, "merged.pdf")
            merger.write(output_path)
            merger.close()
            
            return output_path
        except Exception as e:
            raise Exception(f"Erro ao mesclar PDFs: {str(e)}")
    
    def split_pdf(self, file_path: str, pages: list, output_dir: str) -> str:
        """Dividir PDF em páginas específicas"""
        try:
            reader = PdfReader(file_path)
            writer = PdfWriter()
            
            for page_num in pages:
                if 0 < page_num <= len(reader.pages):
                    writer.add_page(reader.pages[page_num - 1])
            
            output_path = os.path.join(output_dir, "split.pdf")
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            
            return output_path
        except Exception as e:
            raise Exception(f"Erro ao dividir PDF: {str(e)}")
    
    def add_watermark(self, file_path: str, watermark_text: str, output_dir: str) -> str:
        """Adicionar marca d'água ao PDF"""
        try:
            # Criar marca d'água
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont("Helvetica", 40)
            can.setFillColor(Color(0.5, 0.5, 0.5, alpha=0.3))
            can.saveState()
            can.translate(300, 400)
            can.rotate(45)
            can.drawCentredString(0, 0, watermark_text)
            can.restoreState()
            can.save()
            
            packet.seek(0)
            watermark_pdf = PdfReader(packet)
            watermark_page = watermark_pdf.pages[0]
            
            # Aplicar marca d'água em todas as páginas
            reader = PdfReader(file_path)
            writer = PdfWriter()
            
            for page in reader.pages:
                page.merge_page(watermark_page)
                writer.add_page(page)
            
            output_path = os.path.join(output_dir, "watermarked.pdf")
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            
            return output_path
        except Exception as e:
            raise Exception(f"Erro ao adicionar marca d'água: {str(e)}")
    
    def get_pdf_info(self, file_path: str) -> dict:
        """Obter informações do PDF"""
        try:
            reader = PdfReader(file_path)
            return {
                "num_pages": len(reader.pages),
                "metadata": reader.metadata,
                "is_encrypted": reader.is_encrypted
            }
        except Exception as e:
            raise Exception(f"Erro ao obter informações do PDF: {str(e)}")


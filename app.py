from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from typing import Optional, List
import uvicorn

from config import settings
from services.pdf_service import PDFService
from services.ppt_service import PPTService
from services.ai_service import AIService
from services.content_generator import ContentGenerator
from services.large_file_handler import LargeFileHandler

app = FastAPI(
    title="IA Pedagógico",
    description="Plataforma de IA para auxiliar o setor pedagógico na edição de materiais",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serviços
pdf_service = PDFService()
ppt_service = PPTService()
ai_service = AIService()
content_generator = ContentGenerator()
large_file_handler = LargeFileHandler()

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

# ==================== ROTAS PDF ====================

@app.post("/api/pdf/extract-text")
async def extract_text_from_pdf(file: UploadFile = File(...)):
    """Extrair texto de um PDF"""
    try:
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        text = pdf_service.extract_text(file_path)
        return JSONResponse({"success": True, "text": text, "filename": file.filename})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/pdf/merge")
async def merge_pdfs(files: List[UploadFile] = File(...)):
    """Mesclar múltiplos PDFs"""
    try:
        file_paths = []
        for file in files:
            file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_paths.append(file_path)
        
        output_path = pdf_service.merge_pdfs(file_paths, settings.OUTPUT_DIR)
        return FileResponse(output_path, filename="merged.pdf", media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/pdf/split")
async def split_pdf(file: UploadFile = File(...), pages: str = Form(...)):
    """Dividir PDF em páginas específicas"""
    try:
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Converter string de páginas para lista de inteiros
        page_list = [int(p.strip()) for p in pages.split(",")]
        
        output_path = pdf_service.split_pdf(file_path, page_list, settings.OUTPUT_DIR)
        return FileResponse(output_path, filename="split.pdf", media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/pdf/add-watermark")
async def add_watermark_to_pdf(
    file: UploadFile = File(...),
    watermark_text: str = Form(...)
):
    """Adicionar marca d'água ao PDF"""
    try:
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        output_path = pdf_service.add_watermark(file_path, watermark_text, settings.OUTPUT_DIR)
        return FileResponse(output_path, filename="watermarked.pdf", media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ROTAS PPT ====================

@app.post("/api/ppt/create")
async def create_presentation(
    title: str = Form(...),
    slides_content: str = Form(...)
):
    """Criar apresentação PowerPoint"""
    try:
        # slides_content é um JSON string com array de slides
        import json
        slides = json.loads(slides_content)
        
        output_path = ppt_service.create_presentation(title, slides, settings.OUTPUT_DIR)
        return FileResponse(output_path, filename=f"{title}.pptx", 
                          media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ppt/extract-text")
async def extract_text_from_ppt(file: UploadFile = File(...)):
    """Extrair texto de um PowerPoint"""
    try:
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        content = ppt_service.extract_text(file_path)
        return JSONResponse({"success": True, "content": content, "filename": file.filename})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ppt/add-slide")
async def add_slide_to_ppt(
    file: UploadFile = File(...),
    slide_title: str = Form(...),
    slide_content: str = Form(...)
):
    """Adicionar slide a uma apresentação existente"""
    try:
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        output_path = ppt_service.add_slide(file_path, slide_title, slide_content, settings.OUTPUT_DIR)
        return FileResponse(output_path, filename="updated.pptx",
                          media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ROTAS IA ====================

@app.post("/api/ai/improve-text")
async def improve_text(text: str = Form(...), context: str = Form("educacional")):
    """Melhorar texto usando IA"""
    try:
        improved = await ai_service.improve_text(text, context)
        return JSONResponse({"success": True, "improved_text": improved})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/summarize")
async def summarize_text(text: str = Form(...), max_words: int = Form(200)):
    """Resumir texto usando IA"""
    try:
        summary = await ai_service.summarize(text, max_words)
        return JSONResponse({"success": True, "summary": summary})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/generate-questions")
async def generate_questions(
    text: str = Form(...),
    num_questions: int = Form(5),
    difficulty: str = Form("média")
):
    """Gerar questões a partir de um texto"""
    try:
        questions = await ai_service.generate_questions(text, num_questions, difficulty)
        return JSONResponse({"success": True, "questions": questions})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/translate")
async def translate_text(text: str = Form(...), target_language: str = Form("inglês")):
    """Traduzir texto"""
    try:
        translation = await ai_service.translate(text, target_language)
        return JSONResponse({"success": True, "translation": translation})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ROTAS GERADOR DE CONTEÚDO ====================

@app.post("/api/content/lesson-plan")
async def generate_lesson_plan(
    subject: str = Form(...),
    grade: str = Form(...),
    topic: str = Form(...),
    duration: str = Form("50 minutos")
):
    """Gerar plano de aula"""
    try:
        lesson_plan = await content_generator.generate_lesson_plan(subject, grade, topic, duration)
        return JSONResponse({"success": True, "lesson_plan": lesson_plan})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/content/exercise-list")
async def generate_exercises(
    subject: str = Form(...),
    topic: str = Form(...),
    num_exercises: int = Form(10),
    difficulty: str = Form("média")
):
    """Gerar lista de exercícios"""
    try:
        exercises = await content_generator.generate_exercises(subject, topic, num_exercises, difficulty)
        return JSONResponse({"success": True, "exercises": exercises})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/content/presentation-outline")
async def generate_presentation_outline(
    topic: str = Form(...),
    num_slides: int = Form(10),
    audience: str = Form("estudantes")
):
    """Gerar estrutura de apresentação"""
    try:
        outline = await content_generator.generate_presentation_outline(topic, num_slides, audience)
        return JSONResponse({"success": True, "outline": outline})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ROTAS UTILITÁRIAS ====================

@app.get("/api/health")
async def health_check():
    """Verificar saúde da aplicação"""
    return {
        "status": "healthy",
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "anthropic_configured": bool(settings.ANTHROPIC_API_KEY)
    }

# ==================== ROTAS PARA ARQUIVOS GRANDES ====================

@app.post("/api/pdf/extract-text-large")
async def extract_text_from_large_pdf(file: UploadFile = File(...)):
    """Extrair texto de PDF grande (até 25MB)"""
    try:
        # Verificar tamanho
        file_content = await file.read()
        if len(file_content) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="Arquivo muito grande")
        
        # Salvar arquivo temporário
        temp_path = await large_file_handler.save_large_file(file_content, file.filename)
        if not temp_path:
            raise HTTPException(status_code=500, detail="Erro ao processar arquivo")
        
        try:
            # Extrair texto
            text = pdf_service.extract_text(temp_path)
            
            # Se o texto for muito longo, dividir em partes
            if len(text) > 10000:  # 10k caracteres
                chunks = [text[i:i+10000] for i in range(0, len(text), 10000)]
                return JSONResponse({
                    "success": True, 
                    "text": text[:10000],  # Primeira parte
                    "total_chunks": len(chunks),
                    "filename": file.filename,
                    "message": f"Texto extraído em {len(chunks)} partes. Mostrando primeira parte."
                })
            else:
                return JSONResponse({
                    "success": True, 
                    "text": text, 
                    "filename": file.filename
                })
        finally:
            # Limpar arquivo temporário
            large_file_handler.cleanup_temp_file(temp_path)
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/pdf/split-large")
async def split_large_pdf(file: UploadFile = File(...), pages_per_chunk: int = Form(50)):
    """Dividir PDF grande em partes menores"""
    try:
        file_content = await file.read()
        if len(file_content) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="Arquivo muito grande")
        
        temp_path = await large_file_handler.save_large_file(file_content, file.filename)
        if not temp_path:
            raise HTTPException(status_code=500, detail="Erro ao processar arquivo")
        
        try:
            # Dividir PDF
            chunks = large_file_handler.split_large_pdf(temp_path, pages_per_chunk)
            
            if len(chunks) == 1:
                return JSONResponse({
                    "success": True,
                    "message": "PDF não precisa ser dividido",
                    "filename": file.filename
                })
            
            # Criar ZIP com todas as partes
            import zipfile
            zip_path = os.path.join(settings.OUTPUT_DIR, f"split_{file.filename}.zip")
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for i, chunk in enumerate(chunks):
                    zipf.write(chunk, f"parte_{i+1}.pdf")
            
            # Limpar chunks temporários
            for chunk in chunks:
                large_file_handler.cleanup_temp_file(chunk)
            
            return FileResponse(zip_path, filename=f"split_{file.filename}.zip", 
                              media_type="application/zip")
            
        finally:
            large_file_handler.cleanup_temp_file(temp_path)
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/pdf/compress")
async def compress_pdf(file: UploadFile = File(...)):
    """Comprimir PDF para reduzir tamanho"""
    try:
        file_content = await file.read()
        if len(file_content) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="Arquivo muito grande")
        
        temp_path = await large_file_handler.save_large_file(file_content, file.filename)
        if not temp_path:
            raise HTTPException(status_code=500, detail="Erro ao processar arquivo")
        
        try:
            # Comprimir PDF
            compressed_path = large_file_handler.compress_pdf(temp_path)
            
            if compressed_path:
                # Mover para diretório de output
                output_path = os.path.join(settings.OUTPUT_DIR, f"compressed_{file.filename}")
                shutil.move(compressed_path, output_path)
                
                return FileResponse(output_path, filename=f"compressed_{file.filename}", 
                                  media_type="application/pdf")
            else:
                raise HTTPException(status_code=500, detail="Erro ao comprimir PDF")
                
        finally:
            large_file_handler.cleanup_temp_file(temp_path)
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/file-info")
async def get_file_info(filename: str):
    """Obter informações sobre um arquivo"""
    try:
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        
        info = large_file_handler.get_file_info(file_path)
        return JSONResponse({"success": True, "info": info})
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/cleanup")
async def cleanup_files():
    """Limpar arquivos temporários"""
    try:
        for directory in [settings.UPLOAD_DIR, settings.OUTPUT_DIR, settings.TEMP_DIR]:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        return JSONResponse({"success": True, "message": "Arquivos temporários removidos"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", settings.PORT))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=settings.DEBUG)


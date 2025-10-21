import os
from typing import Optional
from config import settings

class AIService:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        
        # Inicializar clientes se as chaves estiverem configuradas
        if settings.OPENAI_API_KEY:
            try:
                from openai import AsyncOpenAI
                self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            except:
                pass
        
        if settings.ANTHROPIC_API_KEY:
            try:
                from anthropic import AsyncAnthropic
                self.anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            except:
                pass
    
    async def _call_ai(self, prompt: str, system_prompt: str = "") -> str:
        """Chamar API de IA (prioriza OpenAI, depois Anthropic)"""
        
        # Tentar OpenAI primeiro
        if self.openai_client:
            try:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                response = await self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2000
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Erro ao chamar OpenAI: {e}")
        
        # Tentar Anthropic se OpenAI falhar ou não estiver configurado
        if self.anthropic_client:
            try:
                full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
                
                response = await self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=2000,
                    temperature=0.7,
                    messages=[{"role": "user", "content": full_prompt}]
                )
                return response.content[0].text
            except Exception as e:
                print(f"Erro ao chamar Anthropic: {e}")
        
        raise Exception("Nenhuma API de IA configurada. Configure OPENAI_API_KEY ou ANTHROPIC_API_KEY no arquivo .env")
    
    async def improve_text(self, text: str, context: str = "educacional") -> str:
        """Melhorar texto usando IA"""
        system_prompt = "Você é um assistente pedagógico especializado em melhorar textos educacionais."
        prompt = f"""
Melhore o seguinte texto no contexto {context}:

{text}

Faça melhorias em:
- Clareza e objetividade
- Gramática e ortografia
- Fluidez e coerência
- Adequação ao público-alvo educacional

Retorne apenas o texto melhorado, sem explicações adicionais.
"""
        return await self._call_ai(prompt, system_prompt)
    
    async def summarize(self, text: str, max_words: int = 200) -> str:
        """Resumir texto usando IA"""
        system_prompt = "Você é um especialista em criar resumos concisos e informativos de textos educacionais."
        prompt = f"""
Crie um resumo do seguinte texto com no máximo {max_words} palavras:

{text}

O resumo deve:
- Capturar os pontos principais
- Ser claro e objetivo
- Manter a essência do conteúdo original
- Ser adequado para uso educacional

Retorne apenas o resumo, sem introduções ou conclusões adicionais.
"""
        return await self._call_ai(prompt, system_prompt)
    
    async def generate_questions(self, text: str, num_questions: int = 5, difficulty: str = "média") -> list:
        """Gerar questões a partir de um texto"""
        system_prompt = "Você é um especialista em criar questões educacionais relevantes e bem estruturadas."
        prompt = f"""
Com base no seguinte texto, crie {num_questions} questões de nível {difficulty}:

{text}

Para cada questão, forneça:
1. A pergunta
2. Quatro alternativas (A, B, C, D)
3. A resposta correta
4. Uma breve explicação

Formate a resposta como uma lista JSON com o seguinte formato:
[
  {{
    "question": "Pergunta aqui?",
    "alternatives": {{
      "A": "Alternativa A",
      "B": "Alternativa B",
      "C": "Alternativa C",
      "D": "Alternativa D"
    }},
    "correct_answer": "A",
    "explanation": "Explicação aqui"
  }}
]

Retorne apenas o JSON, sem texto adicional.
"""
        response = await self._call_ai(prompt, system_prompt)
        
        # Tentar parsear JSON
        import json
        try:
            # Limpar possíveis marcadores de código
            clean_response = response.strip()
            if clean_response.startswith("```"):
                clean_response = clean_response.split("```")[1]
                if clean_response.startswith("json"):
                    clean_response = clean_response[4:]
            clean_response = clean_response.strip()
            
            return json.loads(clean_response)
        except:
            return [{"error": "Não foi possível gerar questões no formato esperado", "raw_response": response}]
    
    async def translate(self, text: str, target_language: str = "inglês") -> str:
        """Traduzir texto"""
        system_prompt = f"Você é um tradutor especializado em textos educacionais."
        prompt = f"""
Traduza o seguinte texto para {target_language}:

{text}

Mantenha:
- O tom educacional
- A formatação
- Termos técnicos apropriados

Retorne apenas a tradução, sem explicações adicionais.
"""
        return await self._call_ai(prompt, system_prompt)
    
    async def correct_grammar(self, text: str) -> str:
        """Corrigir gramática e ortografia"""
        system_prompt = "Você é um especialista em língua portuguesa com foco em textos educacionais."
        prompt = f"""
Corrija os erros gramaticais e ortográficos no seguinte texto:

{text}

Retorne apenas o texto corrigido, sem destacar ou explicar as correções.
"""
        return await self._call_ai(prompt, system_prompt)
    
    async def simplify_text(self, text: str, target_grade: str = "fundamental") -> str:
        """Simplificar texto para um nível de ensino específico"""
        system_prompt = "Você é um especialista em adaptar textos para diferentes níveis educacionais."
        prompt = f"""
Simplifique o seguinte texto para o nível {target_grade}:

{text}

O texto simplificado deve:
- Usar vocabulário apropriado para a faixa etária
- Manter as informações principais
- Ser claro e acessível
- Preservar o valor educacional

Retorne apenas o texto simplificado.
"""
        return await self._call_ai(prompt, system_prompt)


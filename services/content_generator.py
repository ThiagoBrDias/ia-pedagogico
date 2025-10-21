from services.ai_service import AIService

class ContentGenerator:
    def __init__(self):
        self.ai_service = AIService()
    
    async def generate_lesson_plan(self, subject: str, grade: str, topic: str, duration: str) -> dict:
        """Gerar plano de aula completo"""
        system_prompt = "Você é um especialista em planejamento pedagógico."
        prompt = f"""
Crie um plano de aula detalhado com as seguintes características:

- Disciplina: {subject}
- Série/Ano: {grade}
- Tema: {topic}
- Duração: {duration}

O plano de aula deve incluir:
1. Objetivos de aprendizagem (3-5 objetivos)
2. Conteúdos a serem trabalhados
3. Metodologia (como será conduzida a aula)
4. Recursos necessários
5. Desenvolvimento da aula (etapas detalhadas)
6. Avaliação
7. Referências/Bibliografia

Formate como JSON com a seguinte estrutura:
{{
  "title": "Título da Aula",
  "objectives": ["objetivo 1", "objetivo 2", ...],
  "content": "Conteúdos a serem trabalhados",
  "methodology": "Descrição da metodologia",
  "resources": ["recurso 1", "recurso 2", ...],
  "development": [
    {{"step": "Introdução", "duration": "10 min", "description": "..."}},
    {{"step": "Desenvolvimento", "duration": "30 min", "description": "..."}},
    {{"step": "Conclusão", "duration": "10 min", "description": "..."}}
  ],
  "assessment": "Como será feita a avaliação",
  "references": ["referência 1", "referência 2", ...]
}}

Retorne apenas o JSON.
"""
        response = await self.ai_service._call_ai(prompt, system_prompt)
        
        # Parsear JSON
        import json
        try:
            clean_response = response.strip()
            if clean_response.startswith("```"):
                clean_response = clean_response.split("```")[1]
                if clean_response.startswith("json"):
                    clean_response = clean_response[4:]
            clean_response = clean_response.strip()
            
            return json.loads(clean_response)
        except:
            return {"error": "Não foi possível gerar o plano de aula", "raw_response": response}
    
    async def generate_exercises(self, subject: str, topic: str, num_exercises: int, difficulty: str) -> list:
        """Gerar lista de exercícios"""
        system_prompt = "Você é um especialista em criar exercícios educacionais."
        prompt = f"""
Crie uma lista de {num_exercises} exercícios sobre o tema "{topic}" na disciplina de {subject}.

Nível de dificuldade: {difficulty}

Os exercícios devem ser variados e incluir diferentes tipos:
- Múltipla escolha
- Verdadeiro ou falso
- Discursivas
- Resolução de problemas

Para cada exercício, forneça:
1. O enunciado
2. O tipo de exercício
3. A resposta ou gabarito
4. (Opcional) Dica ou explicação

Formate como JSON:
[
  {{
    "number": 1,
    "type": "múltipla escolha",
    "question": "Pergunta?",
    "alternatives": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
    "answer": "A",
    "explanation": "Explicação"
  }},
  {{
    "number": 2,
    "type": "discursiva",
    "question": "Pergunta?",
    "answer": "Resposta esperada",
    "explanation": "Explicação"
  }}
]

Retorne apenas o JSON.
"""
        response = await self.ai_service._call_ai(prompt, system_prompt)
        
        # Parsear JSON
        import json
        try:
            clean_response = response.strip()
            if clean_response.startswith("```"):
                clean_response = clean_response.split("```")[1]
                if clean_response.startswith("json"):
                    clean_response = clean_response[4:]
            clean_response = clean_response.strip()
            
            return json.loads(clean_response)
        except:
            return [{"error": "Não foi possível gerar os exercícios", "raw_response": response}]
    
    async def generate_presentation_outline(self, topic: str, num_slides: int, audience: str) -> list:
        """Gerar estrutura de apresentação"""
        system_prompt = "Você é um especialista em criar apresentações educacionais impactantes."
        prompt = f"""
Crie uma estrutura para uma apresentação sobre "{topic}" com {num_slides} slides.

Público-alvo: {audience}

A estrutura deve incluir:
1. Slide de título
2. Introdução/contextualização
3. Desenvolvimento (vários slides)
4. Conclusão
5. Referências

Para cada slide, forneça:
- Número do slide
- Título
- Pontos principais (bullet points)
- Sugestões de recursos visuais

Formate como JSON:
[
  {{
    "slide_number": 1,
    "title": "Título da Apresentação",
    "content": ["Subtítulo", "Nome do apresentador"],
    "visual_suggestions": "Imagem de fundo relacionada ao tema"
  }},
  {{
    "slide_number": 2,
    "title": "Introdução",
    "content": ["Ponto 1", "Ponto 2", "Ponto 3"],
    "visual_suggestions": "Gráfico ou imagem ilustrativa"
  }}
]

Retorne apenas o JSON.
"""
        response = await self.ai_service._call_ai(prompt, system_prompt)
        
        # Parsear JSON
        import json
        try:
            clean_response = response.strip()
            if clean_response.startswith("```"):
                clean_response = clean_response.split("```")[1]
                if clean_response.startswith("json"):
                    clean_response = clean_response[4:]
            clean_response = clean_response.strip()
            
            return json.loads(clean_response)
        except:
            return [{"error": "Não foi possível gerar a estrutura da apresentação", "raw_response": response}]
    
    async def generate_study_guide(self, subject: str, topics: list, grade: str) -> dict:
        """Gerar guia de estudos"""
        system_prompt = "Você é um especialista em criar materiais de apoio ao estudo."
        topics_text = ", ".join(topics)
        
        prompt = f"""
Crie um guia de estudos para a disciplina de {subject}, série/ano {grade}.

Tópicos a abordar: {topics_text}

O guia deve incluir:
1. Resumo de cada tópico
2. Conceitos-chave
3. Dicas de estudo
4. Questões para reflexão
5. Recursos adicionais recomendados

Formate como JSON com estrutura clara e organizada.

Retorne apenas o JSON.
"""
        response = await self.ai_service._call_ai(prompt, system_prompt)
        
        # Parsear JSON
        import json
        try:
            clean_response = response.strip()
            if clean_response.startswith("```"):
                clean_response = clean_response.split("```")[1]
                if clean_response.startswith("json"):
                    clean_response = clean_response[4:]
            clean_response = clean_response.strip()
            
            return json.loads(clean_response)
        except:
            return {"error": "Não foi possível gerar o guia de estudos", "raw_response": response}


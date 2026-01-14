#!/usr/bin/env python3
"""
Módulo para expandir artículos de noticias a versiones completas y detalladas
Genera artículos periodísticos profesionales con múltiples párrafos
"""

import os
import json
import requests
from dotenv import load_dotenv
from typing import Dict, List
import time

load_dotenv()

API_KEY = os.getenv('BLACKBOX_API_KEY')
API_URL = 'https://api.blackbox.ai/chat/completions'


class ArticleExpander:
    """Expande noticias cortas a artículos periodísticos completos"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or API_KEY
        if not self.api_key:
            raise ValueError("BLACKBOX_API_KEY no encontrada en .env")
        
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        # Estructuras de artículo para variar
        self.structures = [
            "pirámide invertida clásica",  # Lo más importante primero
            "narrativa cronológica",        # Cuenta una historia temporal
            "enfoque analítico",            # Análisis profundo del tema
            "contexto histórico",           # Conecta con eventos pasados
            "impacto y consecuencias",      # Se enfoca en efectos
            "múltiples perspectivas",       # Presenta varios puntos de vista
            "datos y estadísticas",         # Enfoque en números y hechos
            "testimonios y voces"           # Citas y declaraciones
        ]
    
    def expand_article(self, article: Dict, target_words: int = 800, structure: str = None) -> str:
        """
        Expande un artículo corto a uno completo y profesional
        
        Args:
            article: Diccionario con datos del artículo original
            target_words: Número objetivo de palabras (default: 800)
            structure: Estructura narrativa a usar
            
        Returns:
            Artículo expandido completo
        """
        # Extraer información del artículo
        title = article.get('title', '')
        description = article.get('description', '')
        content = article.get('content', '')
        full_text = article.get('full_text', '')
        
        # Manejar source como string o dict
        source_data = article.get('source', {})
        if isinstance(source_data, dict):
            source = article.get('source_name', source_data.get('name', 'Fuente'))
        else:
            source = article.get('source_name', source_data if source_data else 'Fuente')
        
        # Compilar todo el contexto disponible
        context = f"""
Título: {title}

Descripción: {description}

{f"Contenido adicional: {content}" if content else ""}

{f"Texto completo: {full_text}" if full_text else ""}
        """.strip()
        
        structure = structure or self.structures[0]
        
        prompt = f"""Eres un periodista profesional experto. Tu tarea es expandir la siguiente noticia corta 
a un artículo periodístico completo, profesional y creíble de aproximadamente {target_words} palabras.

INFORMACIÓN ORIGINAL:
{context}

INSTRUCCIONES ESPECÍFICAS:
1. Estructura: Usa un enfoque de {structure}
2. Mantén TODOS los hechos y datos del original sin cambiar ninguna información
3. Expande el artículo agregando:
   - Párrafos introductorios sólidos que contextualicen
   - Desarrollo detallado de cada punto mencionado
   - Antecedentes relevantes del tema
   - Posibles implicaciones y consecuencias
   - Contexto tecnológico, industrial o de innovación según corresponda
   - Transiciones naturales entre párrafos
4. Usa un tono periodístico profesional y objetivo
5. Divide en 5-7 párrafos bien estructurados
6. NO inventes cifras, nombres, fechas o declaraciones específicas
7. Mantén la precisión factual - solo expande el contexto y análisis
8. Escribe como si fuera para un periódico de prestigio

IMPORTANTE: 
- NO agregues frases como "según el artículo" o "de acuerdo a la fuente"
- Escribe como si TÚ fueras el periodista que reporta directamente
- NO menciones que estás expandiendo o reescribiendo algo
- Presenta la información con autoridad periodística

Escribe SOLO el artículo expandido, sin introducción ni comentarios:"""

        payload = {
            "model": "blackboxai/meta-llama/llama-3.3-70b-instruct",
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un periodista senior de un medio prestigioso. Escribes artículos profundos, bien investigados y con autoridad."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(API_URL, headers=self.headers, json=payload, timeout=45)
            response.raise_for_status()
            
            result = response.json()
            expanded = result['choices'][0]['message']['content'].strip()
            return expanded
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en API: {e}")
            return f"{title}\n\n{description}\n\n{content or full_text}"
        except (KeyError, IndexError) as e:
            print(f"❌ Error procesando respuesta: {e}")
            return f"{title}\n\n{description}\n\n{content or full_text}"
    
    def expand_with_variations(self, article: Dict, num_variations: int = 3) -> List[Dict]:
        """
        Genera múltiples versiones expandidas del mismo artículo
        
        Args:
            article: Artículo original
            num_variations: Número de versiones a generar
            
        Returns:
            Lista de artículos expandidos con diferentes estructuras
        """
        variations = []
        
        print(f"\n📰 Expandiendo artículo: {article.get('title', 'Sin título')[:60]}...")
        
        for i in range(num_variations):
            structure = self.structures[i % len(self.structures)]
            
            print(f"  [{i+1}/{num_variations}] Estructura: {structure}...", end=" ", flush=True)
            
            expanded_text = self.expand_article(article, target_words=800, structure=structure)
            
            # Extraer título y cuerpo del artículo expandido
            lines = expanded_text.split('\n\n', 1)
            if len(lines) >= 2:
                new_title = lines[0].strip()
                body = lines[1].strip()
            else:
                new_title = article.get('title', '')
                body = expanded_text
            
            # Crear nueva variación con artículo expandido
            variation = article.copy()
            variation['title'] = new_title
            variation['description'] = body.split('\n\n')[0][:300] if '\n\n' in body else body[:300]
            variation['full_text'] = body
            variation['content'] = body[:500]
            variation['expanded'] = True
            variation['expansion_structure'] = structure
            variation['variation_id'] = i + 1
            variation['word_count'] = len(body.split())
            
            variations.append(variation)
            print(f"✅ ({variation['word_count']} palabras)")
            
            # Pausa para no saturar la API
            if (i + 1) % 3 == 0:
                time.sleep(2)
        
        return variations
    
    def process_articles(self, articles: List[Dict], variations_per_article: int = 3) -> List[Dict]:
        """
        Procesa múltiples artículos expandiéndolos
        
        Args:
            articles: Lista de artículos a expandir
            variations_per_article: Número de variaciones por artículo
            
        Returns:
            Lista de todos los artículos expandidos
        """
        all_expanded = []
        
        print(f"\n{'='*70}")
        print(f"📰 EXPANSIÓN DE ARTÍCULOS")
        print(f"{'='*70}")
        print(f"📊 Artículos a procesar: {len(articles)}")
        print(f"📊 Variaciones por artículo: {variations_per_article}")
        print(f"📊 Total artículos expandidos: {len(articles) * variations_per_article}")
        
        for idx, article in enumerate(articles, 1):
            print(f"\n[{idx}/{len(articles)}] Procesando artículo...")
            
            try:
                expanded_variations = self.expand_with_variations(article, variations_per_article)
                all_expanded.extend(expanded_variations)
                
            except Exception as e:
                print(f"❌ Error expandiendo artículo: {e}")
                # Agregar el artículo original si falla
                article_copy = article.copy()
                article_copy['expanded'] = False
                all_expanded.append(article_copy)
        
        print(f"\n{'='*70}")
        print(f"✅ Expansión completada: {len(all_expanded)} artículos generados")
        print(f"{'='*70}")
        
        return all_expanded


def main():
    """Demo del expansor de artículos"""
    import sys
    
    # Artículo de ejemplo para prueba
    sample_article = {
        "title": "Nueva tecnología de IA revoluciona la industria",
        "description": "Científicos presentan un avance significativo en inteligencia artificial que transformará múltiples sectores.",
        "content": "La nueva tecnología permite procesamiento de datos 10 veces más rápido que sistemas anteriores.",
        "source_name": "Tech News",
        "author": "Redacción",
        "url": "https://ejemplo.com/noticia"
    }
    
    # Cargar artículo desde JSON si se proporciona
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    sample_article = data[0]
        except Exception as e:
            print(f"⚠️ No se pudo cargar archivo: {e}")
            print("Usando artículo de ejemplo...")
    
    print("🧪 MODO DEMO - Expansor de Artículos")
    print("="*70)
    
    expander = ArticleExpander()
    expanded_articles = expander.expand_with_variations(sample_article, num_variations=3)
    
    # Guardar resultado
    output_file = 'data/expanded_demo.json'
    os.makedirs('data', exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(expanded_articles, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Resultado guardado en: {output_file}")
    print("\n📄 Vista previa del primer artículo expandido:")
    print("="*70)
    print(expanded_articles[0]['full_text'][:500] + "...")


if __name__ == "__main__":
    main()

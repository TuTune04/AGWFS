"""
AGWFS - Automatically Generate Words For Searching
A tool to generate relevant search keywords using Ollama AI
"""

import os
import json
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class WordGenerator:
    """Generate search keywords using Ollama AI"""
    
    def __init__(self, model: str = None, host: str = None):
        """
        Initialize the WordGenerator
        
        Args:
            model: Ollama model to use (default: from env or 'llama2')
            host: Ollama host URL (default: from env or 'http://localhost:11434')
        """
        self.model = model or os.getenv('OLLAMA_MODEL', 'llama2')
        self.host = host or os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        
    def generate_keywords(self, topic: str, context: str = "general", count: int = 10) -> List[str]:
        """
        Generate search keywords for a given topic
        
        Args:
            topic: The main topic or query
            context: The context (web, academic, shopping, news, etc.)
            count: Number of keywords to generate
            
        Returns:
            List of generated keywords
        """
        try:
            import ollama
            
            prompt = self._build_prompt(topic, context, count)
            
            # Use Ollama to generate keywords
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            
            # Parse the response
            keywords = self._parse_response(response['message']['content'])
            return keywords[:count]
            
        except ImportError:
            print("Warning: ollama package not installed. Using fallback method.")
            return self._fallback_generation(topic, context, count)
        except Exception as e:
            print(f"Error generating keywords with Ollama: {e}")
            print("Using fallback method...")
            return self._fallback_generation(topic, context, count)
    
    def _build_prompt(self, topic: str, context: str, count: int) -> str:
        """Build the prompt for Ollama"""
        context_descriptions = {
            "general": "general web search",
            "academic": "academic research and scholarly articles",
            "shopping": "e-commerce and product search",
            "news": "news articles and current events",
            "technical": "technical documentation and programming",
            "social": "social media content",
            "local": "local businesses and services"
        }
        
        context_desc = context_descriptions.get(context, context)
        
        prompt = f"""Generate {count} relevant search keywords for the topic: "{topic}"

Context: {context_desc}

Requirements:
1. Keywords should be relevant and diverse
2. Include related terms, synonyms, and variations
3. Mix of broad and specific terms
4. Return ONLY the keywords, one per line
5. No numbering, bullets, or explanations

Keywords:"""
        
        return prompt
    
    def _parse_response(self, response: str) -> List[str]:
        """Parse Ollama response to extract keywords"""
        keywords = []
        lines = response.strip().split('\n')
        
        for line in lines:
            # Clean the line
            line = line.strip()
            # Remove common prefixes like numbers, bullets, dashes
            line = line.lstrip('0123456789.-*• ')
            # Remove quotes
            line = line.strip('"\'')
            
            if line and len(line) > 1:
                keywords.append(line)
        
        return keywords
    
    def _fallback_generation(self, topic: str, context: str, count: int) -> List[str]:
        """
        Fallback keyword generation without Ollama
        Uses simple word expansion and related terms
        """
        keywords = [topic]
        
        # Add some basic variations
        words = topic.lower().split()
        
        # Add individual words
        keywords.extend([w for w in words if len(w) > 2])
        
        # Add combinations
        if len(words) > 1:
            keywords.append(' '.join(words[:2]))
            keywords.append(' '.join(words[-2:]))
        
        # Add context-specific terms
        context_terms = {
            "academic": ["research", "study", "analysis", "journal", "paper"],
            "shopping": ["buy", "price", "review", "best", "cheap"],
            "news": ["latest", "breaking", "update", "today", "report"],
            "technical": ["documentation", "tutorial", "guide", "api", "how to"],
            "social": ["trending", "viral", "popular", "discussion", "community"],
            "local": ["near me", "nearby", "location", "address", "hours"]
        }
        
        if context in context_terms:
            for term in context_terms[context][:3]:
                keywords.append(f"{topic} {term}")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for k in keywords:
            k_lower = k.lower()
            if k_lower not in seen:
                seen.add(k_lower)
                unique_keywords.append(k)
        
        return unique_keywords[:count]
    
    def generate_with_synonyms(self, topic: str, count: int = 10) -> Dict[str, List[str]]:
        """
        Generate keywords with synonyms and related terms
        
        Args:
            topic: The main topic
            count: Number of keyword groups to generate
            
        Returns:
            Dictionary with main keywords and their synonyms
        """
        try:
            import ollama
            
            prompt = f"""For the topic "{topic}", generate {count} main keywords and for each keyword provide 2-3 synonyms or related terms.

Format the response as:
keyword1: synonym1, synonym2, synonym3
keyword2: synonym1, synonym2, synonym3

Topic: {topic}
Keywords with synonyms:"""
            
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            return self._parse_synonym_response(response['message']['content'])
            
        except Exception as e:
            print(f"Error: {e}. Using fallback.")
            keywords = self.generate_keywords(topic, count=count)
            return {k: [k] for k in keywords}
    
    def _parse_synonym_response(self, response: str) -> Dict[str, List[str]]:
        """Parse response containing keywords with synonyms"""
        result = {}
        lines = response.strip().split('\n')
        
        for line in lines:
            if ':' in line:
                parts = line.split(':', 1)
                keyword = parts[0].strip().lstrip('0123456789.-*• ')
                synonyms_str = parts[1].strip()
                synonyms = [s.strip() for s in synonyms_str.split(',')]
                
                if keyword and synonyms:
                    result[keyword] = synonyms
        
        return result


def main():
    """Main entry point for the word generator"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='AGWFS - Automatically Generate Words For Searching using Ollama'
    )
    parser.add_argument('topic', type=str, help='Topic or query to generate keywords for')
    parser.add_argument('-c', '--context', type=str, default='general',
                       choices=['general', 'academic', 'shopping', 'news', 'technical', 'social', 'local'],
                       help='Search context (default: general)')
    parser.add_argument('-n', '--count', type=int, default=10,
                       help='Number of keywords to generate (default: 10)')
    parser.add_argument('-s', '--synonyms', action='store_true',
                       help='Generate keywords with synonyms')
    parser.add_argument('-m', '--model', type=str, default=None,
                       help='Ollama model to use (default: from env or llama2)')
    parser.add_argument('-o', '--output', type=str, choices=['text', 'json'],
                       default='text', help='Output format (default: text)')
    
    args = parser.parse_args()
    
    generator = WordGenerator(model=args.model)
    
    print(f"Generating keywords for: '{args.topic}'")
    print(f"Context: {args.context}")
    print(f"Using model: {generator.model}")
    print("-" * 50)
    
    if args.synonyms:
        results = generator.generate_with_synonyms(args.topic, args.count)
        
        if args.output == 'json':
            print(json.dumps(results, indent=2))
        else:
            for keyword, synonyms in results.items():
                print(f"\n{keyword}:")
                for syn in synonyms:
                    print(f"  - {syn}")
    else:
        keywords = generator.generate_keywords(args.topic, args.context, args.count)
        
        if args.output == 'json':
            print(json.dumps(keywords, indent=2))
        else:
            print("\nGenerated keywords:")
            for i, keyword in enumerate(keywords, 1):
                print(f"{i}. {keyword}")


if __name__ == '__main__':
    main()

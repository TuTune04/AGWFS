"""
Simple API wrapper for AGWFS
Makes it easy to integrate word generation into your applications
"""

from word_generator import WordGenerator
from typing import List, Dict, Optional


class AGWFS:
    """
    Simple API wrapper for Automatically Generate Words For Searching
    
    Example:
        >>> from agwfs import AGWFS
        >>> agwfs = AGWFS()
        >>> keywords = agwfs.search_keywords("machine learning")
        >>> print(keywords)
    """
    
    def __init__(self, model: str = None, host: str = None):
        """
        Initialize AGWFS
        
        Args:
            model: Ollama model to use (optional)
            host: Ollama host URL (optional)
        """
        self.generator = WordGenerator(model=model, host=host)
    
    def search_keywords(
        self,
        topic: str,
        count: int = 10,
        context: str = "general"
    ) -> List[str]:
        """
        Generate search keywords for a topic
        
        Args:
            topic: The search topic
            count: Number of keywords to generate
            context: Search context (general, academic, shopping, etc.)
            
        Returns:
            List of keyword strings
        """
        return self.generator.generate_keywords(topic, context, count)
    
    def technical_keywords(self, topic: str, count: int = 10) -> List[str]:
        """Generate keywords for technical/programming searches"""
        return self.search_keywords(topic, count, "technical")
    
    def shopping_keywords(self, topic: str, count: int = 10) -> List[str]:
        """Generate keywords for e-commerce/shopping searches"""
        return self.search_keywords(topic, count, "shopping")
    
    def academic_keywords(self, topic: str, count: int = 10) -> List[str]:
        """Generate keywords for academic research"""
        return self.search_keywords(topic, count, "academic")
    
    def news_keywords(self, topic: str, count: int = 10) -> List[str]:
        """Generate keywords for news searches"""
        return self.search_keywords(topic, count, "news")
    
    def local_keywords(self, topic: str, count: int = 10) -> List[str]:
        """Generate keywords for local business searches"""
        return self.search_keywords(topic, count, "local")
    
    def keywords_with_related_terms(
        self,
        topic: str,
        count: int = 5
    ) -> Dict[str, List[str]]:
        """
        Generate keywords with related terms and synonyms
        
        Args:
            topic: The search topic
            count: Number of keyword groups to generate
            
        Returns:
            Dictionary mapping keywords to lists of related terms
        """
        return self.generator.generate_with_synonyms(topic, count)


# Convenience functions for quick use
def generate_keywords(topic: str, count: int = 10, context: str = "general") -> List[str]:
    """
    Quick function to generate keywords
    
    Args:
        topic: The search topic
        count: Number of keywords (default: 10)
        context: Search context (default: general)
        
    Returns:
        List of keywords
    """
    agwfs = AGWFS()
    return agwfs.search_keywords(topic, count, context)


def technical_search(topic: str, count: int = 10) -> List[str]:
    """Quick technical keyword generation"""
    return generate_keywords(topic, count, "technical")


def shopping_search(topic: str, count: int = 10) -> List[str]:
    """Quick shopping keyword generation"""
    return generate_keywords(topic, count, "shopping")


def academic_search(topic: str, count: int = 10) -> List[str]:
    """Quick academic keyword generation"""
    return generate_keywords(topic, count, "academic")


if __name__ == '__main__':
    # Quick demo
    print("AGWFS API Demo\n")
    
    # Using the class
    agwfs = AGWFS()
    
    print("1. Technical keywords for 'Python programming':")
    keywords = agwfs.technical_keywords("Python programming", 5)
    for kw in keywords:
        print(f"   - {kw}")
    
    print("\n2. Shopping keywords for 'laptop':")
    keywords = agwfs.shopping_keywords("laptop", 5)
    for kw in keywords:
        print(f"   - {kw}")
    
    # Using convenience functions
    print("\n3. Academic keywords using quick function:")
    keywords = academic_search("climate change", 5)
    for kw in keywords:
        print(f"   - {kw}")

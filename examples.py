#!/usr/bin/env python3
"""
Example usage of AGWFS word generator
"""

from word_generator import WordGenerator


def example_basic():
    """Basic keyword generation example"""
    print("=" * 60)
    print("Example 1: Basic Keyword Generation")
    print("=" * 60)
    
    generator = WordGenerator()
    keywords = generator.generate_keywords("machine learning", context="technical", count=8)
    
    print("\nTopic: 'machine learning'")
    print("Context: technical")
    print("\nGenerated keywords:")
    for i, keyword in enumerate(keywords, 1):
        print(f"  {i}. {keyword}")


def example_shopping():
    """E-commerce keyword generation example"""
    print("\n" + "=" * 60)
    print("Example 2: Shopping Keywords")
    print("=" * 60)
    
    generator = WordGenerator()
    keywords = generator.generate_keywords("wireless headphones", context="shopping", count=10)
    
    print("\nTopic: 'wireless headphones'")
    print("Context: shopping")
    print("\nGenerated keywords:")
    for i, keyword in enumerate(keywords, 1):
        print(f"  {i}. {keyword}")


def example_academic():
    """Academic research keyword generation example"""
    print("\n" + "=" * 60)
    print("Example 3: Academic Research Keywords")
    print("=" * 60)
    
    generator = WordGenerator()
    keywords = generator.generate_keywords("climate change", context="academic", count=8)
    
    print("\nTopic: 'climate change'")
    print("Context: academic")
    print("\nGenerated keywords:")
    for i, keyword in enumerate(keywords, 1):
        print(f"  {i}. {keyword}")


def example_with_synonyms():
    """Keyword generation with synonyms example"""
    print("\n" + "=" * 60)
    print("Example 4: Keywords with Synonyms")
    print("=" * 60)
    
    generator = WordGenerator()
    results = generator.generate_with_synonyms("artificial intelligence", count=5)
    
    print("\nTopic: 'artificial intelligence'")
    print("\nGenerated keywords with synonyms:")
    for keyword, synonyms in results.items():
        print(f"\n  {keyword}:")
        for syn in synonyms:
            print(f"    - {syn}")


def example_multiple_contexts():
    """Show keyword generation across different contexts"""
    print("\n" + "=" * 60)
    print("Example 5: Same Topic, Different Contexts")
    print("=" * 60)
    
    topic = "python"
    contexts = ["technical", "shopping", "academic"]
    
    generator = WordGenerator()
    
    for context in contexts:
        keywords = generator.generate_keywords(topic, context=context, count=5)
        print(f"\nContext: {context}")
        print(f"Keywords for '{topic}':")
        for i, keyword in enumerate(keywords, 1):
            print(f"  {i}. {keyword}")


if __name__ == '__main__':
    print("\nAGWFS - Automatically Generate Words For Searching")
    print("Example Usage Demonstrations\n")
    
    # Run all examples
    example_basic()
    example_shopping()
    example_academic()
    example_with_synonyms()
    example_multiple_contexts()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print("\nTo use the CLI:")
    print("  python word_generator.py 'your topic' -c technical -n 10")
    print("\nFor help:")
    print("  python word_generator.py --help")

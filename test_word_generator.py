"""
Tests for AGWFS word generator
"""

import unittest
from word_generator import WordGenerator


class TestWordGenerator(unittest.TestCase):
    """Test cases for WordGenerator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = WordGenerator()
    
    def test_initialization(self):
        """Test WordGenerator initialization"""
        self.assertIsNotNone(self.generator.model)
        self.assertIsNotNone(self.generator.host)
    
    def test_generate_keywords_basic(self):
        """Test basic keyword generation"""
        keywords = self.generator.generate_keywords("python programming", count=5)
        
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)
        self.assertLessEqual(len(keywords), 5)
        
        # Check that all keywords are strings
        for keyword in keywords:
            self.assertIsInstance(keyword, str)
            self.assertGreater(len(keyword), 0)
    
    def test_generate_keywords_different_contexts(self):
        """Test keyword generation with different contexts"""
        contexts = ['general', 'academic', 'shopping', 'technical']
        
        for context in contexts:
            keywords = self.generator.generate_keywords(
                "machine learning",
                context=context,
                count=5
            )
            self.assertIsInstance(keywords, list)
            self.assertGreater(len(keywords), 0)
    
    def test_generate_keywords_count(self):
        """Test that the count parameter is respected"""
        counts = [3, 5, 10, 15]
        
        for count in counts:
            keywords = self.generator.generate_keywords(
                "test topic",
                count=count
            )
            self.assertLessEqual(len(keywords), count)
    
    def test_fallback_generation(self):
        """Test fallback keyword generation"""
        keywords = self.generator._fallback_generation(
            "artificial intelligence",
            "technical",
            10
        )
        
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)
        self.assertLessEqual(len(keywords), 10)
    
    def test_generate_with_synonyms(self):
        """Test keyword generation with synonyms"""
        results = self.generator.generate_with_synonyms("coding", count=3)
        
        self.assertIsInstance(results, dict)
        self.assertGreater(len(results), 0)
        
        # Check structure
        for keyword, synonyms in results.items():
            self.assertIsInstance(keyword, str)
            self.assertIsInstance(synonyms, list)
            self.assertGreater(len(keyword), 0)
    
    def test_parse_response(self):
        """Test response parsing"""
        test_response = """1. keyword one
2. keyword two
3. keyword three"""
        
        keywords = self.generator._parse_response(test_response)
        
        self.assertEqual(len(keywords), 3)
        self.assertEqual(keywords[0], "keyword one")
        self.assertEqual(keywords[1], "keyword two")
        self.assertEqual(keywords[2], "keyword three")
    
    def test_parse_response_with_bullets(self):
        """Test parsing response with different bullet styles"""
        test_response = """- keyword one
* keyword two
• keyword three"""
        
        keywords = self.generator._parse_response(test_response)
        
        self.assertGreaterEqual(len(keywords), 3)
        self.assertIn("keyword one", keywords)
        self.assertIn("keyword two", keywords)
        self.assertIn("keyword three", keywords)
    
    def test_build_prompt(self):
        """Test prompt building"""
        prompt = self.generator._build_prompt("test topic", "general", 5)
        
        self.assertIsInstance(prompt, str)
        self.assertIn("test topic", prompt)
        self.assertIn("5", prompt)
        self.assertGreater(len(prompt), 0)
    
    def test_empty_topic(self):
        """Test handling of empty topic"""
        keywords = self.generator.generate_keywords("", count=5)
        
        self.assertIsInstance(keywords, list)
    
    def test_unique_keywords(self):
        """Test that generated keywords are unique"""
        keywords = self.generator.generate_keywords("python", count=10)
        
        # Check for duplicates (case-insensitive)
        lowercase_keywords = [k.lower() for k in keywords]
        self.assertEqual(len(lowercase_keywords), len(set(lowercase_keywords)))


class TestPromptBuilding(unittest.TestCase):
    """Test prompt building functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = WordGenerator()
    
    def test_prompt_includes_topic(self):
        """Test that prompt includes the topic"""
        prompt = self.generator._build_prompt("machine learning", "general", 10)
        self.assertIn("machine learning", prompt)
    
    def test_prompt_includes_count(self):
        """Test that prompt includes the count"""
        prompt = self.generator._build_prompt("test", "general", 7)
        self.assertIn("7", prompt)
    
    def test_different_contexts(self):
        """Test prompts for different contexts"""
        contexts = ['academic', 'shopping', 'news', 'technical']
        
        for context in contexts:
            prompt = self.generator._build_prompt("test", context, 5)
            self.assertIsInstance(prompt, str)
            self.assertGreater(len(prompt), 0)


if __name__ == '__main__':
    unittest.main()

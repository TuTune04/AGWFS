# Using AGWFS with Ollama Cloud Free

This guide shows how to use AGWFS with Ollama's cloud free tier.

## Quick Start with Ollama Cloud

### Option 1: Local Ollama (Recommended for Best Results)

1. **Install Ollama** from [ollama.ai](https://ollama.ai)

2. **Pull a model** (e.g., llama2, which is free):
   ```bash
   ollama pull llama2
   ```

3. **Start Ollama**:
   ```bash
   ollama serve
   ```

4. **Use AGWFS** with default settings:
   ```bash
   python word_generator.py "machine learning" -c technical -n 10
   ```

### Option 2: Fallback Mode (No Ollama Installation)

AGWFS works even without Ollama installed! It will use a built-in fallback method:

```bash
python word_generator.py "wireless headphones" -c shopping -n 8
```

**Note:** While the fallback mode works, using Ollama provides much better and more diverse keyword suggestions.

## Configuration for Cloud Endpoint

If you have access to an Ollama cloud endpoint, configure it:

1. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your cloud endpoint:
   ```env
   OLLAMA_HOST=https://your-ollama-cloud-endpoint.com
   OLLAMA_MODEL=llama2
   ```

3. Run AGWFS:
   ```bash
   python word_generator.py "your topic"
   ```

## Available Models

With Ollama (local or cloud), you can use various models:

- **llama2** (recommended, free, good balance)
- **llama3** (more advanced, if available)
- **mistral** (fast and efficient)
- **codellama** (optimized for technical/code topics)

Use a specific model:
```bash
python word_generator.py "python programming" -m mistral -c technical
```

## Best Practices

### 1. Choose the Right Context

Different contexts produce different keyword styles:

```bash
# For coding/programming topics
python word_generator.py "REST API" -c technical

# For shopping/products
python word_generator.py "running shoes" -c shopping

# For research
python word_generator.py "quantum computing" -c academic

# For news/current events
python word_generator.py "climate summit" -c news
```

### 2. Adjust Count for Your Needs

```bash
# Quick search (5-8 keywords)
python word_generator.py "topic" -n 5

# Comprehensive search (15-20 keywords)
python word_generator.py "topic" -n 20
```

### 3. Use Synonyms for SEO

Generate keywords with synonyms for better SEO coverage:
```bash
python word_generator.py "artificial intelligence" -s -n 5
```

### 4. JSON Output for Integration

Get JSON output for easy integration with other tools:
```bash
python word_generator.py "machine learning" -c technical -n 10 -o json > keywords.json
```

## Using the Python API

### Basic Usage

```python
from word_generator import WordGenerator

generator = WordGenerator()

# Generate keywords
keywords = generator.generate_keywords(
    topic="cloud computing",
    context="technical",
    count=10
)

print("Keywords:", keywords)
```

### Using the Simple API Wrapper

```python
from agwfs import AGWFS

agwfs = AGWFS()

# Quick methods
tech_keywords = agwfs.technical_keywords("Python programming", 10)
shop_keywords = agwfs.shopping_keywords("laptop", 8)
academic_keywords = agwfs.academic_keywords("climate change", 12)
```

### Convenience Functions

```python
from agwfs import generate_keywords, technical_search, shopping_search

# One-liner usage
keywords = technical_search("machine learning")
products = shopping_search("wireless mouse")
topics = generate_keywords("artificial intelligence", count=15, context="academic")
```

## Performance Tips

### 1. Local Ollama is Faster

Local Ollama installations are typically faster than cloud endpoints due to network latency.

### 2. Model Selection

- Use **llama2** for general purpose (good balance)
- Use **codellama** for technical/programming topics
- Use **mistral** if you need speed

### 3. Caching Results

For repeated searches, cache results:

```python
from word_generator import WordGenerator
import json

generator = WordGenerator()

# Generate once
keywords = generator.generate_keywords("topic", "technical", 10)

# Save for reuse
with open("cached_keywords.json", "w") as f:
    json.dump(keywords, f)

# Load when needed
with open("cached_keywords.json", "r") as f:
    cached_keywords = json.load(f)
```

## Troubleshooting

### "Connection refused" Error

If you see connection errors:

1. Check if Ollama is running:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. Start Ollama if needed:
   ```bash
   ollama serve
   ```

3. Or use fallback mode (automatic)

### "Model not found" Error

Pull the model first:
```bash
ollama pull llama2
```

### Slow Response Times

- Use a smaller model (llama2 vs llama3)
- Reduce keyword count
- Use fallback mode for quick results

## Free Tier Limitations

When using Ollama cloud free tier:

- ✅ Unlimited local usage
- ✅ Basic models (llama2, mistral)
- ⚠️ Cloud endpoints may have rate limits
- ⚠️ Advanced models may require paid tier

**Recommendation:** Use local Ollama for unlimited, fast, and free keyword generation!

## Examples Gallery

### E-commerce SEO
```bash
python word_generator.py "organic coffee beans" -c shopping -n 15 -o json
```

### Blog Post Research
```bash
python word_generator.py "sustainable living tips" -c general -n 12
```

### Academic Paper Keywords
```bash
python word_generator.py "neural networks" -c academic -s
```

### Local Business Search
```bash
python word_generator.py "Italian restaurant" -c local -n 8
```

### Technical Documentation
```bash
python word_generator.py "Docker containers" -c technical -n 10
```

## Integration Examples

### With Search APIs

```python
from agwfs import generate_keywords
import requests

# Generate keywords
keywords = generate_keywords("machine learning", count=5, context="technical")

# Use with search API
for keyword in keywords:
    results = requests.get(f"https://api.search.com?q={keyword}")
    print(f"Results for '{keyword}':", results.json())
```

### With SEO Tools

```python
from agwfs import AGWFS
import csv

agwfs = AGWFS()

# Generate for multiple topics
topics = ["AI", "cloud computing", "cybersecurity"]

with open("seo_keywords.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Topic", "Keywords"])
    
    for topic in topics:
        keywords = agwfs.technical_keywords(topic, 10)
        writer.writerow([topic, ", ".join(keywords)])
```

## Summary

AGWFS with Ollama cloud free provides:

- 🆓 **Free keyword generation**
- 🚀 **Fast and efficient**
- 🎯 **Context-aware results**
- 💪 **Flexible integration**
- 🔧 **Easy to use**

Start generating better search keywords today!

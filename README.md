# AGWFS - Automatically Generate Words For Searching

🔍 A powerful tool to automatically generate relevant search keywords using Ollama AI (cloud free tier compatible).

## Features

- 🤖 **AI-Powered**: Uses Ollama AI models for intelligent keyword generation
- 🎯 **Context-Aware**: Supports multiple search contexts (general, academic, shopping, news, technical, social, local)
- 🔄 **Synonym Generation**: Generate keywords with related terms and synonyms
- 🌐 **Cloud Compatible**: Works with Ollama cloud free tier
- 📦 **Easy to Use**: Simple CLI and Python API
- ⚡ **Fallback Mode**: Works even without Ollama installed

## Installation

### Prerequisites

1. **Python 3.7 or higher**

2. **Ollama** (optional but recommended):
   - For local use: Install from [ollama.ai](https://ollama.ai)
   - For cloud use: Access Ollama cloud free tier
   - Pull a model: `ollama pull llama2`

### Setup

1. Clone the repository:
```bash
git clone https://github.com/TuTune04/AGWFS.git
cd AGWFS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Configure environment variables:
```bash
cp .env.example .env
# Edit .env to set your Ollama host and model
```

## Usage

### Command Line Interface

Basic usage:
```bash
python word_generator.py "your search topic"
```

With options:
```bash
# Generate technical keywords
python word_generator.py "machine learning" -c technical -n 15

# Generate shopping keywords
python word_generator.py "wireless headphones" -c shopping -n 10

# Generate keywords with synonyms
python word_generator.py "artificial intelligence" -s -n 5

# Output as JSON
python word_generator.py "python programming" -o json
```

### Command Line Options

- `topic`: The main topic or query (required)
- `-c, --context`: Search context (choices: general, academic, shopping, news, technical, social, local)
- `-n, --count`: Number of keywords to generate (default: 10)
- `-s, --synonyms`: Generate keywords with synonyms
- `-m, --model`: Ollama model to use (default: llama2)
- `-o, --output`: Output format (choices: text, json)

### Python API

```python
from word_generator import WordGenerator

# Initialize generator
generator = WordGenerator()

# Generate keywords
keywords = generator.generate_keywords(
    topic="machine learning",
    context="technical",
    count=10
)

for keyword in keywords:
    print(keyword)

# Generate keywords with synonyms
results = generator.generate_with_synonyms("AI", count=5)
for keyword, synonyms in results.items():
    print(f"{keyword}: {', '.join(synonyms)}")
```

### Examples

Run the examples script to see various use cases:
```bash
python examples.py
```

## Contexts

Different contexts optimize keyword generation for specific use cases:

- **general**: General web search
- **academic**: Academic research and scholarly articles
- **shopping**: E-commerce and product search
- **news**: News articles and current events
- **technical**: Technical documentation and programming
- **social**: Social media content
- **local**: Local businesses and services

## Configuration

### Environment Variables

Create a `.env` file with:

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
```

### Using Ollama Cloud Free

To use Ollama cloud free tier:
1. Set `OLLAMA_HOST` to the cloud endpoint
2. Ensure you have access to the free tier
3. The tool will automatically connect

### Using Local Ollama

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull a model: `ollama pull llama2`
3. Start Ollama: `ollama serve`
4. Use default settings or set `OLLAMA_HOST=http://localhost:11434`

## Testing

Run the test suite:
```bash
python -m unittest test_word_generator.py
```

Run specific tests:
```bash
python -m unittest test_word_generator.TestWordGenerator.test_generate_keywords_basic
```

## How It Works

1. **Input Processing**: Takes your topic and context
2. **Prompt Engineering**: Creates optimized prompts for Ollama
3. **AI Generation**: Uses Ollama AI to generate relevant keywords
4. **Post-Processing**: Cleans and formats the output
5. **Fallback Mode**: If Ollama is unavailable, uses rule-based generation

## Benefits

- ✅ Save time on keyword research
- ✅ Discover related terms you might miss
- ✅ Context-aware suggestions
- ✅ Free to use with Ollama cloud
- ✅ Works offline with local Ollama
- ✅ Extensible and customizable

## Troubleshooting

### Ollama Connection Issues

If you get connection errors:
```bash
# Check if Ollama is running
ollama list

# Start Ollama
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

### No Ollama Installed

The tool will automatically fall back to rule-based generation if Ollama is not available. For best results, install Ollama.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Support

- 📧 Issues: [GitHub Issues](https://github.com/TuTune04/AGWFS/issues)
- 📖 Documentation: This README
- 💡 Examples: See `examples.py`

## Acknowledgments

- Built with [Ollama](https://ollama.ai) - Free AI models
- Inspired by the need for better keyword research tools

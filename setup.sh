#!/bin/bash
# Setup script for AGWFS

echo "================================"
echo "AGWFS Setup Script"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies."
    exit 1
fi

echo ""
echo "Creating environment configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env file created. You can edit it to configure Ollama settings."
else
    echo ".env file already exists."
fi

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Quick Start:"
echo "  1. (Optional) Install Ollama: https://ollama.ai"
echo "  2. (Optional) Pull a model: ollama pull llama2"
echo "  3. Run examples: python examples.py"
echo "  4. Try CLI: python word_generator.py 'your topic' -c technical"
echo ""
echo "For help: python word_generator.py --help"
echo ""

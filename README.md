![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-yellow.svg)

# Meeting Minutes Generator

This project transcribes meeting audio using OpenAI's Whisper API and generates professional meeting minutes using a Llama-based model. The minutes are then provided as a downloadable PDF.

This app transcribes meeting audio using OpenAI’s Whisper API 🎙️ and leverages a Llama-based model to generate professional meeting minutes. It even supports generating minutes in Markdown format with a refined, formal style, featuring:

A concise summary with attendees, location, and date 📅

Detailed discussion points and key takeaways 🔍

Clearly defined action items with respective owners ✅

All meeting minutes are then provided as a downloadable PDF, making follow-ups and record keeping easier than ever.


## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/frezazadeh/Meeting-Minutes-Generator.git
    cd Meeting-Minutes-Generator
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file and add your API key:
    ```
    OPENAI_API_KEY=your_openai_api_key
    HF_TOKEN=your_HF_TOKEN_api_key
    ```

## Usage

Run the application:
```bash
python main.py

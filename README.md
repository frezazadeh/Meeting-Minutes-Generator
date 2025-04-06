# Meeting Minutes Generator

This project transcribes meeting audio using OpenAI's Whisper API and generates professional meeting minutes using a Llama-based model. The minutes are then provided as a downloadable PDF.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file and add your OpenAI API key:
    ```
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

Run the application:
```bash
python main.py

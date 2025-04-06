import os
import uuid
import torch
import openai
from dotenv import load_dotenv
from fpdf import FPDF
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

class MeetingMinutesGenerator:
    """
    A class to handle transcription of audio meetings using OpenAI's Whisper model
    and generation of meeting minutes via a Llama-based model.
    """

    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OpenAI API Key not set.")
        openai.api_key = self.openai_api_key

        # Model configurations
        self.AUDIO_MODEL = "whisper-1"
        self.LLAMA_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"

        # Initialize tokenizer and model with quantization configuration for efficiency
        self.tokenizer = AutoTokenizer.from_pretrained(self.LLAMA_MODEL)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_quant_type="nf4"
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.LLAMA_MODEL,
            device_map="auto",
            quantization_config=quant_config
        )

    def transcribe_audio(self, audio_path: str, progress=None) -> str:
        """
        Transcribe the provided MP3 audio file using OpenAI's Whisper model.
        """
        if progress:
            progress(0.3, desc="Transcribing audio...")
        try:
            with open(audio_path, "rb") as audio_file:
                transcription = openai.Audio.transcribe(
                    self.AUDIO_MODEL,
                    audio_file,
                    response_format="text"
                )
                return transcription
        except Exception as e:
            return f"Error during transcription: {str(e)}"

    def generate_minutes(self, transcription: str, progress=None) -> str:
        """
        Generate meeting minutes in markdown from a transcription using the Llama model.
        """
        if progress:
            progress(0.6, desc="Generating meeting minutes...")

        # Updated system prompt for a more professional style
        system_message = (
            "You are a professional meeting minutes writer. "
            "Generate meeting minutes in markdown format with a refined, formal style. "
            "Include a concise summary with attendees, location, and date; detailed discussion points; "
            "key takeaways; and clearly defined action items with respective owners."
        )
        user_prompt = (
            f"Below is an extract transcript of a meeting. Please write professional meeting minutes in markdown "
            f"including the requested sections.\n{transcription}"
        )
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ]

        # Prepare input and generate output
        inputs = self.tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
        outputs = self.model.generate(inputs, max_new_tokens=2000)
        response = self.tokenizer.decode(outputs[0])
        if progress:
            progress(0.9, desc="Finalizing minutes...")
        # Clean up the output to remove extraneous tokens if present
        cleaned_response = response.split("<|end_header_id|>")[-1].strip().replace("<|eot_id|>", "")
        return cleaned_response

    def generate_pdf(self, minutes_text: str) -> str:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        # Using multi_cell for automatic text wrapping
        for line in minutes_text.split('\n'):
            pdf.multi_cell(0, 10, txt=line)
        pdf_file = f"meeting_minutes_{uuid.uuid4().hex}.pdf"
        pdf.output(pdf_file)
        return pdf_file

    def process_upload(self, audio_file: str, progress=None):
        """
        Process an uploaded MP3 file: transcribe the audio, generate meeting minutes,
        and create a downloadable PDF file. Yields intermediate progress messages.
        Returns a tuple of (meeting minutes in markdown, PDF file path).
        """
        if not audio_file:
            yield ("Please upload an audio file.", None)
            return

        # Check file extension
        if not str(audio_file).lower().endswith('.mp3'):
            yield ("Please upload an MP3 file.", None)
            return

        yield ("Starting process...", None)
        if progress:
            progress(0.1, desc="Starting process...")

        transcription = self.transcribe_audio(audio_file, progress=progress)
        if isinstance(transcription, str) and transcription.startswith("Error"):
            yield (transcription, None)
            return

        yield ("Audio transcribed. Generating meeting minutes...", None)
        minutes = self.generate_minutes(transcription, progress=progress)

        # Generate PDF file from the minutes text
        pdf_file = self.generate_pdf(minutes)
        if progress:
            progress(1.0, desc="Process complete!")
        yield (minutes, pdf_file)

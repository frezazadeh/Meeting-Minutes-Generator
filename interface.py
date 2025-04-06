import gradio as gr
from meeting_minutes_generator import MeetingMinutesGenerator

def launch_interface():
    """
    Initialize the MeetingMinutesGenerator and launch the Gradio interface with an advanced GUI.
    """
    generator = MeetingMinutesGenerator()

    # Custom CSS for a more advanced and polished look
    css = """
    body {
        background: #f7f7f7;
        font-family: 'Arial', sans-serif;
    }
    .gradio-container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-radius: 8px;
    }
    h1 {
        text-align: center;
        color: #333;
    }
    """

    with gr.Blocks(css=css) as demo:
        gr.Markdown("# Meeting Minutes Generator")
        gr.Markdown("Upload an MP3 recording of your meeting or record the meeting to generate AI-driven, professional meeting minutes and a downloadable PDF.")
        with gr.Row():
            audio_input = gr.Audio(type="filepath", label="Upload MP3 File", format="mp3")
        with gr.Row():
            markdown_output = gr.Markdown(label="Meeting Minutes")
        with gr.Row():
            pdf_output = gr.File(label="Download PDF")
        with gr.Row():
            submit_btn = gr.Button("Submit")
        submit_btn.click(fn=generator.process_upload, inputs=audio_input, outputs=[markdown_output, pdf_output])
    # Enable queueing for streaming generator outputs, then launch
    demo.queue().launch(inbrowser=True)

import os

import requests
import gradio as gr
from gradio.themes import Soft

FASTAPI_URL = os.getenv('FASTAPI_URL', 'http://localhost:8000')
PREDICT_URL = f"{FASTAPI_URL}/predict"


def predict_via_api(text) -> str:
    """Send a request to the FastAPI backend for sentiment prediction"""
    try:
        response = requests.post(
            PREDICT_URL,
            json={"text": text},
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            sentiment = result["sentiment"]
            confidence = result["confidence"]
            
            emoji = "😊" if sentiment == "positive" else "😞"
            return f"{emoji} {sentiment.upper()}\nConfidence: {confidence:.2%}"
        else:
            return f"❌ API Error: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "❌ Could not connect to API. Make sure FastAPI is running."
    except Exception as e:
        return f"❌ Error: {str(e)}"


with gr.Blocks(title="IMDB Sentiment Analysis", theme=Soft()) as demo:
    gr.Markdown("# 🎬 IMDB Review Sentiment Analysis")
    gr.Markdown("Enter a movie review, and the model will predict its sentiment.")

    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Your Review",
                placeholder="Write your review here...",
                lines=5
            )
            submit_btn = gr.Button("🚀 Analyze", variant="primary")
        
        with gr.Column():
            output_text = gr.Textbox(label="Result", lines=3)
    
    gr.Examples(
        examples=[
            ["This movie was absolutely wonderful! I loved it."],
            ["Terrible film, complete waste of time."],
            ["It was okay, not great but not bad."],
        ],
        inputs=text_input
    )
    
    submit_btn.click(
        fn=predict_via_api,
        inputs=text_input,
        outputs=output_text
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
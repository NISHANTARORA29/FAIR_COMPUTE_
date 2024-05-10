import requests
import json
import gradio as gr
from PIL import Image
import base64

# Assuming your image captioning API expects base64 encoded images
def encode_image(image_path):
    try:
        with Image.open(image_path) as img:
            img_byte_array = img.convert('RGB').tobytes()
            img_base64 = base64.b64encode(img_byte_array).decode('utf-8')
            return img_base64
    except FileNotFoundError:
        print("Error: Image file not found.")
        return None

url = "http://8.12.5.44:11434/api/generate"

headers = {
    'Content-Type': 'application/json'
}
history = []

def generate_response(prompt, image=None):
    history.append(prompt)
    final_prompt = "\n".join(history)

    data = {
        "model": "llava",
        "prompt": final_prompt,
        "stream": False
    }

    if image:
        encoded_image = encode_image(image)
        if encoded_image:
            data["image"] = encoded_image  # Add encoded image to request data

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response = response.text
        data = json.loads(response)
        actual_response = data['response']
        return actual_response
    else:
        print("Error:", response.text)

interface = gr.Interface(
    fn=generate_response,
    inputs=[gr.Textbox(lines=2, placeholder="Enter your prompt (optional)"),
            gr.Image(type="pil")],  # Add image input
    outputs="text"
)

interface.launch()

from flask import Flask, request, jsonify, render_template
from PIL import Image
import base64
import requests
import json

app = Flask(__name__)

# Assuming your image captioning API expects base64 encoded images
def encode_image(image):
    if isinstance(image, str):  # If image is a file path
        try:
            with Image.open(image) as img:
                img_byte_array = img.convert('RGB').tobytes()
                img_base64 = base64.b64encode(img_byte_array).decode('utf-8')
                return img_base64
        except FileNotFoundError:
            print("Error: Image file not found.")
            return None
    elif isinstance(image, Image.Image):  # If image is a PIL Image object
        img_byte_array = image.convert('RGB').tobytes()
        img_base64 = base64.b64encode(img_byte_array).decode('utf-8')
        return img_base64
    else:
        print("Error: Invalid image format.")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        image = request.files['image'] if 'image' in request.files else None
        response = generate_response(prompt, image)
        return render_template('index.html', response=response)
    return render_template('index.html')

def generate_response(prompt, image=None):
    url = "http://127.0.0.1:11434/api/generate"
    headers = {'Content-Type': 'application/json'}
    history = []
    
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
        return "Error: Failed to generate response."

if __name__ == '__main__':
    app.run(debug=True)

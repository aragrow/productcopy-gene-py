import os
import urllib.request
from flask import Flask, request, jsonify
from PIL import Image
import google.generativeai as genai
import requests
from urllib.parse import urlparse
import sys

#curl -X POST http://127.0.0.1:5000/describe-image -F "image=http://localhost:10053/wp-content/uploads/2024/12/cedarchest-e1733586383484.png"
sys.stdout.write('Exec: Script')

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, I am Python!"

@app.route('/describe-image', methods=['POST'])
def describe_image():
    print('Exec->describe_image()')
    if request.method == 'POST':
        try:

            uri = request.form.get('image')
            prompt = request.form.get('prompt')
            
            project_id = "gen-lang-client-0011860578"
            credentials_path = "../gemini_service_account.json"
            
            parsed_url = urlparse(uri)
            if not parsed_url.path:
                return None
            image_filename =  parsed_url.path.split('/')[-1]  # Get the last part of the path

            images_dir = "downloaded"

            os.makedirs(images_dir, exist_ok=True)

            # Combine directory and filename
            full_filename = os.path.join(images_dir, image_filename)

            sys.stdout.write(full_filename)
            
            # Download and save the file
            local_filename, headers = urllib.request.urlretrieve(uri, full_filename)
            print(f"File saved as: {local_filename}")
            print(f"Headers: {headers}")

            img = Image.open(full_filename)

            model = genai.GenerativeModel('gemini-1.5-flash')

            response = model.generate_content([prompt, img], stream=True)

            response.resolve()

            description = response.text

            # Clean up the temporary image
            os.remove(full_filename)

            # Return the description
            return jsonify({"status":True,"description": description})       

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return 'Invalid request method'

# End of function describe_image()

@app.route('/generate-post', methods=['POST'])
def generate_post():
    print('Exec->generate_post()')
    if request.method == 'POST':
        try:
            # Check if an image file is provided 
            
            description = request.form.get('description')
            postTitle = request.form.get('post_title')
            postContent = request.form.get('post_content')
           # attributes = request.form.get('attributes')
            prompt = request.form.get('prompt')

            project_id = "gen-lang-client-0011860578"
            credentials_path = "../gemini_service_account.json"

            print('Prompt: ')
            print(prompt)

            attrs = {
                'description' : description,
                'post_title' : postTitle,
                'post_content' : postContent
            }
            
            print(attrs)
            print(type(attrs))

            model = genai.GenerativeModel('gemini-1.5-flash')
            content = {
                "parts": [
                    {
                        "text": prompt  # This is the main text prompt
                    },
                    {
                        "text": f"Description: {description}\nPost Title: {postTitle}"  # Additional context (e.g., description, title)
                    }
                ]
            }

            response = model.generate_content(content, stream=True)
            
            print('Response:')
            print(response)

            response.resolve()

            description = response.text

            # Return the description
            return jsonify({"status":True,"description": description})       

        except Exception as e:
            print({"error": str(e)})
            return jsonify({"error": str(e)}), 500

    else:
        return 'Invalid request method'

# End of function generate_post()

@app.route('/execute-prompt', methods=['POST'])
def execute_prompt():
    print('Exec->execute_prompt())')
    if request.method == 'POST':
        try:

            uri = request.form.get('image')
            post = request.form.get('post')
            title = request.form.get('title')
            prompt = request.form.get('prompt')
            
            print(f'Promt: -->{prompt}')
            project_id = "gen-lang-client-0011860578"
            credentials_path = "../gemini_service_account.json"
            
            print(f'URI: -->{uri}')
            parsed_url = urlparse(uri)
            if not parsed_url.path:
                return None
            image_filename =  parsed_url.path.split('/')[-1]  # Get the last part of the path

            images_dir = "./downloaded"
            print(f'Directory: -->{images_dir}')

            os.makedirs(images_dir, exist_ok=True)

            # Combine directory and filename
            full_filename = os.path.join(images_dir, image_filename)

            sys.stdout.write(full_filename)

            local_filename, headers = urllib.request.urlretrieve(uri, full_filename)
            print(f"File saved as: {local_filename}")
            print(f"Headers: {headers}")

            img = Image.open(full_filename)

            model = genai.GenerativeModel('gemini-1.5-flash')

            response = model.generate_content([prompt, img], stream=True)

            response.resolve()

            description = response.text
            print(f'Description:\n{description}')
            # Clean up the temporary image
            os.remove(full_filename)

            # Return the description
            return jsonify({"status":True,"description": description})       

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return 'Invalid request method'

if __name__ == '__main__':
    app.run(debug=True)
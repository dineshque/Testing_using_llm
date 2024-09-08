import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)
# Folder to store uploaded images temporarily
UPLOAD_FOLDER = 'ScreenShot'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed extensions for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/describe', methods=['POST'])
def describe_testing_instructions():
    print("Started")
    # Get the text context from the form data
    context = request.form.get('context', '')

    # Handle image uploads
    images = request.files.getlist('screenshots')

    if not images:
        return jsonify({'error': 'No images uploaded'}), 400

    # Validate and save images (for demo, we won't actually process the images)
    image_paths = []
    for image in images:
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_paths.append(image_path)
        else:
            return jsonify({'error': 'Invalid file type'}), 400

    # Simulated response for testing instructions (mocking the output of the OpenAI API)
    simulated_response = [
        {
            "Description": "Test case for source and destination selection.",
            "Pre-conditions": "The user must have the app installed and logged in.",
            "Testing Steps": [
                "Open the app.",
                "Navigate to the bus booking screen.",
                "Enter the source location.",
                "Enter the destination location.",
                "Select a travel date."
            ],
            "Expected Result": "The app should display a list of available buses for the selected route and date."
        },
    ]
    print("End")
    return jsonify({'test_cases': simulated_response})

if __name__ == '__main__':
    app.run(debug=True)

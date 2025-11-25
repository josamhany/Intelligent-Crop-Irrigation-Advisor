import os
from flask import Flask, render_template, request
from src.pipeline.predict_pipeline import PredictPipeline
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Run prediction pipeline
        predictor = PredictPipeline()
        prediction = predictor.predict(file_path)

        return render_template('index.html', prediction=f"Predicted Soil Type: {prediction}", image_path=file_path)

if __name__ == "__main__":
    print("Starting Flask server at http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)

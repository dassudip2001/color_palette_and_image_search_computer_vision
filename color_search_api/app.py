from flask import Flask, request, jsonify,render_template
import numpy as np
import cv2

app = Flask(__name__)
app.name = 'color_search_api'

def get_dominant_color(height, width, color):
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = color
    red, green, blue = int(color[2]), int(color[1]), int(color[0])
    return bar, (red, green, blue)
# web app
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# health check
@app.route('/api', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

@app.route('/get_dominant_colors', methods=['POST'])
def get_dominant_colors():
    # Check if an image file is provided
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    # Check if the file is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # Check if the file is an image
    if not file.filename.endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({'error': 'Unsupported file format'})

    # Read the image
    nparr = np.fromstring(file.read(), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # extract the height, width, and the number of channels of the image
    height, width, _ = np.shape(img)

    # reshape the image to a 2D array of pixels and 3 color values (RGB)
    data = np.reshape(img, (height * width, 3))
    data = np.float32(data)

    # clustering
    number_of_clusters = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(data, number_of_clusters, None, criteria, 10, flags)

    # Get dominant colors
    dominant_colors = []
    for index, row in enumerate(centers):
        _, rgb = get_dominant_color(200, 200, row)
        dominant_colors.append(rgb)

    return jsonify({'dominant_colors': dominant_colors})

if __name__ == '__main__':
    app.run(debug=True)

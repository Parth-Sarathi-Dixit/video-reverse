from flask import Flask, render_template, request, send_from_directory
import os
import cv2
app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return 'No files uploaded'

    file = request.files['video']

    if file.filename == '':
        return 'No file selected'

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    reversed_filename = reverse_video(file.filename)

    return send_from_directory(app.config['UPLOAD_FOLDER'], reversed_filename, as_attachment=True)


def reverse_video(filename):
    # Video reversal logic using OpenCV
    # Load the video using OpenCV
    cap = cv2.VideoCapture(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Get video properties
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    # Determine the output file path for the reversed video
    reversed_filename = 'reversed_' + filename
    reversed_filepath = os.path.join(
        app.config['UPLOAD_FOLDER'], reversed_filename)

    # Create a VideoWriter to save the reversed video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use appropriate codec
    out = cv2.VideoWriter(reversed_filepath, fourcc,
                          fps, (int(width), int(height)))

    # Read and write frames in reverse order
    for i in range(int(frames)-1, -1, -1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        out.write(frame)

    # Release resources
    cap.release()
    out.release()

    return reversed_filename

    # Add your code here to reverse the video using the provided filename
    # Return the filename of the reversed video


if __name__ == "__main__":
    app.run(debug=True)

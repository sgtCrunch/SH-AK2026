import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ── Config ────────────────────────────────────────────────
UPLOAD_FOLDER   = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ── Sample data — replace with your own source ────────────
ITEMS = [
    "🌟 You are braver than you believe",
    "💫 Strength lies in the journey, not the destination",
    "🌙 Every night ends with a new dawn",
    "✨ Small steps lead to great distances",
    "🌊 Flow with change, grow with challenge",
    "🔥 Passion fuels the extraordinary",
    "🌺 Kindness is a language everyone understands",
    "🦋 Transformation begins from within",
    "🌈 After every storm comes colour",
    "💎 Your potential is limitless",
    "🌿 Growth is not always visible, but it is always happening",
    "⚡ Energy flows where attention goes",
    "🎯 Focus on progress, not perfection",
    "🌸 Bloom wherever you are planted",
    "🔮 The future belongs to the curious",
]

ITEMS_PER_PAGE = 5


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ── Routes ────────────────────────────────────────────────
@app.route('/')
def index():
    pages = [ITEMS[i:i + ITEMS_PER_PAGE]
             for i in range(0, len(ITEMS), ITEMS_PER_PAGE)]
    return render_template('envelope.html', pages=pages)


@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['photo']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename  = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Avoid overwriting — append a counter if needed
        base, ext = os.path.splitext(filename)
        counter   = 1
        while os.path.exists(save_path):
            filename  = f'{base}_{counter}{ext}'
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            counter  += 1

        file.save(save_path)
        url = f'/static/uploads/{filename}'
        return jsonify({'url': url, 'filename': filename})

    return jsonify({'error': 'File type not allowed'}), 400


if __name__ == '__main__':
    app.run(debug=True)

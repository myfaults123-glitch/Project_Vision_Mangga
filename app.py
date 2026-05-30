import os
import cv2
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from ultralytics import YOLO

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Membuat folder otomatis jika belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Memanggil otak AI dari dalam folder runs
model = YOLO('runs/detect/train_mangga_v9/weights/best.pt')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Tidak ada file yang diunggah"
        
        file = request.files['file']
        if file.filename == '':
            return "File kosong"

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Deteksi mangga
            results = model.predict(source=filepath, conf=0.40)
            
            matang = 0
            mengkal = 0
            mentah = 0

            # Hitung jumlah per kelas
            for r in results:
                for c in r.boxes.cls:
                    class_name = model.names[int(c)]
                    if class_name == 'matang': matang += 1
                    elif class_name == 'mengkal': mengkal += 1
                    elif class_name == 'mentah': mentah += 1
            
            # Gambar kotak dan simpan
            result_img = results[0].plot()
            result_filename = "result_" + filename
            result_filepath = os.path.join(app.config['RESULT_FOLDER'], result_filename)
            cv2.imwrite(result_filepath, result_img)

            # Kirim hasil ke website
            return render_template('index.html', 
                                   result_image=result_filename,
                                   matang=matang, mengkal=mengkal, mentah=mentah)

    return render_template('index.html', result_image=None)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
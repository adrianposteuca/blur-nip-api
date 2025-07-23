import io
from flask import Flask
from flask import request, send_file
from PIL import Image, ImageFilter
from ultralytics import YOLO

app = Flask(__name__)

print("Se încarcă modelul AI...")
model = YOLO('erax-ai/EraX-Anti-NSFW-V1.1')
print("Modelul AI a fost încărcat cu succes.")

@app.route('/api/blur-nipples', methods=['POST'])
def blur_nipples_endpoint():
    if 'image' not in request.files:
        return "Eroare: Niciun fișier imagine nu a fost trimis.", 400

    image_file = request.files['image']
    img = Image.open(image_file).convert("RGB")
    
    # MODIFICARE: Citim noii parametri din cerere, cu valori implicite
    # parseInt pentru a ne asigura ca sunt numere
    try:
        blur_radius = int(request.form.get('blur_radius', 35))
        padding = int(request.form.get('padding', 15)) # Padding în pixeli
    except ValueError:
        return "Eroare: blur_radius și padding trebuie să fie numere întregi.", 400

    results = model(img)

    # MODIFICARE: Preluăm dimensiunile imaginii pentru a nu depăși marginile
    img_width, img_height = img.size

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            class_name = model.names[class_id]
            
            if class_name == 'nipple':
                coords = box.xyxy[0].tolist()
                x1, y1, x2, y2 = int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])

                # MODIFICARE: Aplicăm padding-ul la coordonate, cu verificare a limitelor
                padded_x1 = max(0, x1 - padding)
                padded_y1 = max(0, y1 - padding)
                padded_x2 = min(img_width, x2 + padding)
                padded_y2 = min(img_height, y2 + padding)

                box_coords = (padded_x1, padded_y1, padded_x2, padded_y2)
                
                # Asigurăm că avem o zonă validă de decupat
                if box_coords[0] < box_coords[2] and box_coords[1] < box_coords[3]:
                    crop = img.crop(box_coords)
                    # MODIFICARE: Folosim raza de blur dinamică
                    blurred_crop = crop.filter(ImageFilter.GaussianBlur(radius=blur_radius))
                    img.paste(blurred_crop, box_coords)

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

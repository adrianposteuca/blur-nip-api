import io
from flask import Flask
from flask import request, send_file
from PIL import Image, ImageFilter, ImageOps
from ultralytics import YOLO

app = Flask(__name__)

# Încărcăm modelul AI
print("Se încarcă modelul AI...")
model = YOLO('erax-anti-nsfw-yolo11n-v1.1.pt')
print("Modelul AI a fost încărcat cu succes.")

@app.route('/api/blur-nipples', methods=['POST'])
def blur_nipples_endpoint():
    if 'image' not in request.files:
        return "Eroare: Niciun fișier imagine nu a fost trimis.", 400

    image_file = request.files['image']
    img = Image.open(image_file).convert("RGB")
    
    try:
        # Citim toți parametrii din cerere, cu valori implicite
        rotation = int(request.form.get('rotation', 0))
        scale = float(request.form.get('scale', 1.0))
        confidence = float(request.form.get('confidence', 0.70))
        blur_radius = int(request.form.get('blur_radius', 35))
        size_selector = int(request.form.get('padding', 0))

        print(f"--- Cerere Nouă ---")
        print(f"Valori primite -> Rotation: {rotation}, Scale: {scale}, Confidence: {confidence}")
        print(f"Valori primite -> Blur Radius: {blur_radius}, Size Selector: {size_selector}")

    except ValueError:
        return "Eroare: parametrii trebuie să fie numere valide.", 400

    # Aplicăm rotația, dacă este specificată
    if rotation in [90, 180, 270]:
        img = img.rotate(-rotation, expand=True)
        print(f"Imaginea a fost rotită cu {rotation} grade.")

    # Aplicăm scalarea, dacă este specificată
    if scale < 1.0 and scale > 0:
        original_width, original_height = img.size
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        print(f"Imaginea a fost scalată la {new_width}x{new_height} pixeli.")

    results = model(img, verbose=False) # Am adăugat verbose=False pentru log-uri mai curate
    img_width, img_height = img.size

    print("Analizând rezultatele detecției...")
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            class_name = model.names[class_id]
            confidence_score = float(box.conf)
            
            # Verificăm clasa și pragul de încredere
            if class_name == 'nipple' and confidence_score >= confidence:
                print(f"Detecție 'nipple' cu încredere de {confidence_score:.2f} (peste pragul de {confidence:.2f})")
                coords = box.xyxy[0].tolist()
                x1, y1, x2, y2 = int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])
                
                original_width = x2 - x1
                original_height = y2 - y1
                print(f"Dimensiune Originală detectată: {original_width}x{original_height} pixeli")

                if size_selector == 0:
                    final_box_coords = (x1, y1, x2, y2)
                else:
                    target_size = size_selector * 100
                    half_size = target_size / 2
                    center_x = x1 + original_width / 2
                    center_y = y1 + original_height / 2
                    new_x1 = int(center_x - half_size)
                    new_y1 = int(center_y - half_size)
                    new_x2 = int(center_x + half_size)
                    new_y2 = int(center_y + half_size)
                    final_box_coords = (max(0, new_x1), max(0, new_y1), min(img_width, new_x2), min(img_height, new_y2))
                
                final_width = final_box_coords[2] - final_box_coords[0]
                final_height = final_box_coords[3] - final_box_coords[1]
                print(f"Dimensiune Finală pentru blur: {final_width}x{final_height} pixeli")
                
                if final_box_coords[0] < final_box_coords[2] and final_box_coords[1] < final_box_coords[3]:
                    crop = img.crop(final_box_coords)
                    blurred_crop = crop.filter(ImageFilter.GaussianBlur(radius=blur_radius))
                    img.paste(blurred_crop, final_box_coords)

    print("Procesare finalizată. Se returnează imaginea.")
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

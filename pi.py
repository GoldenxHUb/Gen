import os
from flask import Flask, request, jsonify
from PIL import Image, ImageEnhance, ImageFilter
import requests
import io

app = Flask(__name__)

@app.route('/getpixels', methods=['GET'])
def get_pixels():
    image_url = request.args.get('url')
    if not image_url:
        return jsonify({"error": "Missing URL"}), 400

    response = requests.get(image_url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to load image"}), 500

    img = Image.open(io.BytesIO(response.content)).convert("RGB")

    # Resize image using LANCZOS for better quality
    img = img.resize((400, 400), Image.Resampling.LANCZOS)

    # Enhance sharpness (can adjust the factor)
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.0)  # You can try different values for sharpness

    # Apply UnsharpMask filter to further enhance sharpness
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    width, height = img.size
    pixels = [[img.getpixel((x, y)) for x in range(width)] for y in range(height)]

    return jsonify({
        "width": width,
        "height": height,
        "pixels": pixels
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

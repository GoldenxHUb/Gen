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

    # เปิดภาพและแปลงเป็น RGB
    img = Image.open(io.BytesIO(response.content)).convert("RGB")
    
    # ใช้ฟิลเตอร์ UnsharpMask เพื่อเพิ่มความคมชัด
    sharpness_filter = ImageFilter.UnsharpMask(radius=2, percent=200, threshold=2)
    img = img.filter(sharpness_filter)
    
    # เพิ่มคอนทราสต์ของภาพ
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)  # เพิ่มคอนทราสต์ 50%
    
    # เพิ่มความคมชัดอีกครั้ง
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.0)  # เพิ่มความคมชัด 100%

    # ปรับขนาดภาพเป็น 339x194
    img = img.resize((339, 194), Image.LANCZOS)  # ใช้ LANCZOS เพื่อให้ภาพชัดสุด

    width, height = img.size

    # ดึงข้อมูลพิกเซลจากภาพ
    pixels = [[img.getpixel((x, y)) for x in range(width)] for y in range(height)]

    return jsonify({
        "width": width,
        "height": height, 
        "pixels": pixels
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

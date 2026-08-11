import sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps
import numpy as np

def prep_photo(input_path="source-photo.jpg", output_path="source-prepped.png"):
    inp = Path(input_path)
    if not inp.exists():
        print(f"Error: {input_path} does not exist.")
        return

    print(f"Prepping {input_path}...")
    img = Image.open(inp).convert("RGBA")
    
    bg_removed = None
    try:
        from rembg import remove
        print("Removing background with rembg...")
        bg_removed = remove(img)
    except Exception as e:
        print(f"rembg warning: {e}. Proceeding with original image layout.")
        bg_removed = img

    white_bg = Image.new("RGBA", bg_removed.size, (255, 255, 255, 255))
    composite = Image.alpha_composite(white_bg, bg_removed).convert("L")

    try:
        import cv2
        np_arr = np.array(composite)
        clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8, 8))
        enhanced_np = clahe.apply(np_arr)
        enhanced_img = Image.fromarray(enhanced_np)
    except Exception as e:
        print(f"OpenCV CLAHE warning: {e}. Using PIL contrast enhancement.")
        enhancer = ImageEnhance.Contrast(composite)
        enhanced_img = enhancer.enhance(1.8)

    enhanced_img.save(output_path)
    print(f"Saved prepped image to {output_path}")

if __name__ == "__main__":
    photo_file = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep_photo(photo_file)

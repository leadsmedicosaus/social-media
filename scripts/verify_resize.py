
import os
import sys
from pathlib import Path
from PIL import Image

# Add project root to python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from integrations.helpers.image_processor.make_image_postable import resize_image

def verify_resize():
    # Use an existing image or create a dummy one
    input_image_path = project_root / "static/johns-weather-forecating-stone.jpg"
    
    # If the file doesn't exist (it should, based on ls output), create a dummy one
    if not input_image_path.exists():
        print(f"Warning: {input_image_path} not found. Creating a dummy image.")
        img = Image.new('RGB', (800, 600), color='red')
        input_image_path = project_root / "test_input.jpg"
        img.save(input_image_path)

    # Output path
    output_image_path = project_root / "test_resized.jpg"
    
    # Copy input to output to simulate the inplace modification or new file creation logic
    # The resize_image function modifies the file in place or returns a new path
    # But looking at the code: resize_image(image_path, ...) returns image_path
    
    # Let's use a temporary copy for testing to avoid overwriting the original static asset
    import shutil
    shutil.copy(input_image_path, output_image_path)

    print(f"Resizing {output_image_path}...")
    try:
        resize_image(str(output_image_path))
        
        # Check dimensions
        with Image.open(output_image_path) as img:
            print(f"Resized image dimensions: {img.size}")
            if img.size == (1080, 1350):
                print("SUCCESS: Image resized to 1080x1350")
            else:
                print(f"FAILURE: Image dimensions are {img.size}, expected (1080, 1350)")
                
    except Exception as e:
        print(f"Error during resizing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_resize()

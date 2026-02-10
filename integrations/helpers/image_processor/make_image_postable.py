import os
import uuid
import shutil
import tempfile
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from core.logger import log, send_notification
from .pexels import get_relevant_image_for_text


def resize_image_width(image_path: str, target_width: int = 1080):
    img = Image.open(image_path)

    # Calculate new height to maintain aspect ratio
    original_width, original_height = img.size
    aspect_ratio = original_height / original_width
    new_height = int(target_width * aspect_ratio)

    # Resize the image
    resized_img = img.resize((target_width, new_height), Image.LANCZOS)
    resized_img.save(image_path)

    return image_path


def resize_image(image_path: str, image_bg: str = None, target_width: int = 1080, target_height: int = 1350):
    # Open and convert the main image to RGB
    img = Image.open(image_path).convert("RGB")
    
    # Calculate target and image aspect ratios
    target_aspect = target_width / target_height
    img_aspect = img.width / img.height

    if img_aspect > target_aspect:
        # Image is wider than target frame — match height, then crop width
        new_height = target_height
        new_width = int(new_height * img_aspect)
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Calculate cropping box for width
        left = (new_width - target_width) // 2
        top = 0
        right = left + target_width
        bottom = target_height
    else:
        # Image is taller than target frame — match width, then crop height
        new_width = target_width
        new_height = int(new_width / img_aspect)
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Calculate cropping box for height
        left = 0
        top = (new_height - target_height) // 2
        right = target_width
        bottom = top + target_height

    # Crop the image to the exact target dimensions
    final_img = resized_img.crop((left, top, right, bottom))
    
    # Save the final image
    final_img.save(image_path)
    return image_path


def create_image_from_text(
    text: str,
    image_path: str = None,
    width: int = 1080,
    font_size: int = 40,
    padding: int = 40,
    background_color: str = "black",
    text_color: str = "white",
):
    if image_path is None:
        temp_dir = tempfile.mkdtemp()
        image_path = os.path.join(temp_dir, f"{uuid.uuid4()}.png")
    
    font_path = Path(__file__).parent / "Inter_28pt-SemiBold.ttf"
    font = ImageFont.truetype(font_path, font_size)

    # Calculate how much space we have for text
    text_width = width - (2.3 * padding)

    # Split the text by newlines first to preserve manual line breaks
    paragraphs = text.split("\n")

    # Then wrap each paragraph to fit width
    all_lines = []
    for paragraph in paragraphs:
        if paragraph.strip():
            # Wrap non-empty paragraphs
            wrapped_lines = textwrap.wrap(
                paragraph, width=int(text_width / (font_size * 0.5))
            )
            all_lines.extend(wrapped_lines)
        else:
            # Preserve empty lines
            all_lines.append("")

    # Calculate height based on number of lines
    line_height = font_size * 1.5
    text_height = len(all_lines) * line_height
    height = int(text_height + (2 * padding))

    # Create image
    image = Image.new("RGB", (width, height), color=background_color)
    draw = ImageDraw.Draw(image)

    # Draw text
    y_position = padding
    for line in all_lines:
        draw.text((padding, y_position), line, font=font, fill=text_color)
        y_position += line_height

    image.save(image_path)

    return image_path


def concat_image_vertically(
    image_path: str, top_image_path: str, bottom_image_path: str
):
    top_img = Image.open(top_image_path)
    bottom_img = Image.open(bottom_image_path)

    # Create a new image with the height being the sum of both images' heights
    combined_height = top_img.height + bottom_img.height
    combined_img = Image.new("RGB", (top_img.width, combined_height))

    # Paste the first image at the top
    combined_img.paste(top_img, (0, 0))

    # Paste the second image below the first one
    combined_img.paste(bottom_img, (0, top_img.height))

    combined_img.save(image_path)
    return image_path


def create_image(*, image_path: str = None, text: str = None):
    # If we have an image, just resize it (don't add text to image)
    if image_path:
        resized_image_path = resize_image(image_path)
        return resized_image_path

    # If only text (no image), create an image from text with background
    if text and not image_path:
        text_image_path = create_image_from_text(text)
        bg_image_path = get_relevant_image_for_text(text)
        resized_image_path = resize_image(text_image_path, bg_image_path)
        os.remove(bg_image_path)
        return resized_image_path

    raise Exception("Image or text must be provided!")


def make_image_postable(image_path: str = None, text: str = None):
    try:
        created_image_path = create_image(image_path=image_path, text=text)
        return created_image_path
    except Exception as err:
        log.exception(err)
        send_notification(email="ImPosting", message=str(err))
        return image_path

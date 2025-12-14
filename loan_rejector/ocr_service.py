import easyocr
from PIL import Image
import os
import io

def extract_text_from_image(image_path, lang_list=['en']):
    """
    Extracts text from an image file using EasyOCR with specified languages.
    
    Args:
        image_path (str): Path to the image file.
        lang_list (list): List of language codes (e.g., ['en', 'es']).
        
    Returns:
        str: Extracted text from the image.
    """
    if not os.path.exists(image_path):
        return f"Error: Image file not found at {image_path}"
    
    try:
        # Initialize reader (this acts as a singleton in practice if cached, 
        # but initializing here is safer for script execution)
        reader = easyocr.Reader(lang_list, verbose=False) 
        
        # Read text
        # detail=0 returns just the list of string results
        result = reader.readtext(image_path, detail=0)
        
        return " ".join(result)
    except Exception as e:
        return f"Error processing image with EasyOCR: {str(e)}"

if __name__ == "__main__":
    # Test block
    print("OCR Service Test")

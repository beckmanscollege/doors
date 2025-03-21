import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import json

def convert_to_serializable(obj):
    if hasattr(obj, 'numerator') and hasattr(obj, 'denominator'):
        return float(obj.numerator) / float(obj.denominator)
    return str(obj)

def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        exif = image._getexif()
        if not exif:
            return None

        exif_data = {}
        for tag_id in exif:
            tag = TAGS.get(tag_id, tag_id)
            data = exif.get(tag_id)
            
            # Hantera bytes
            if isinstance(data, bytes):
                try:
                    for encoding in ['utf-8', 'latin1', 'cp1252']:
                        try:
                            data = data.decode(encoding)
                            break
                        except UnicodeDecodeError:
                            continue
                except:
                    data = data.hex()
            
            # Hantera tupler och andra komplexa typer
            if isinstance(data, (tuple, list)):
                data = [convert_to_serializable(item) for item in data]
            else:
                data = convert_to_serializable(data)
                
            exif_data[tag] = data

        return exif_data
    except Exception as e:
        print(f"Error reading {image_path}: {str(e)}")
        return None

def main():
    door_dir = "door"
    results = {}
    
    for filename in os.listdir(door_dir):
        if filename.lower().endswith('.jpg'):
            filepath = os.path.join(door_dir, filename)
            exif_data = get_exif_data(filepath)
            if exif_data:
                results[filename] = exif_data
    
    # Spara resultaten till en JSON-fil
    with open('exif_data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Processed {len(results)} images. Results saved to exif_data.json")

if __name__ == "__main__":
    main() 
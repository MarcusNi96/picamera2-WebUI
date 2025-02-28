import os
import json
from datetime import datetime
from PIL import Image

def grid_crop(full_image_path, output_dir, rows, columns, crop_square_size, common_labels=None):
    """
    Perform grid cropping on a full-resolution image.
    
    Parameters:
        full_image_path (str): Path to the captured image.
        output_dir (str): Directory where cropped images and metadata will be saved.
        rows (int): Number of rows in the grid.
        columns (int): Number of columns in the grid.
        crop_square_size (int): The width and height of each square crop.
        common_labels (dict): Optional metadata labels.
    
    Returns:
        dict: Metadata of the grid cropping operation.
    """
    with Image.open(full_image_path) as img:
        width, height = img.size

        total_crop_width = columns * crop_square_size
        total_crop_height = rows * crop_square_size
        # Center the grid in the original image
        x_padding = max((width - total_crop_width) // 2, 0)
        y_padding = max((height - total_crop_height) // 2, 0)

        cropped_mapping = {}
        os.makedirs(output_dir, exist_ok=True)

        session_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Optionally, save the full image in the session folder
        full_image_filename = f"full_{session_timestamp}.jpg"
        img.save(os.path.join(output_dir, full_image_filename))
        
        for row in range(rows):
            for col in range(columns):
                left = x_padding + col * crop_square_size
                upper = y_padding + row * crop_square_size
                right = left + crop_square_size
                lower = upper + crop_square_size
                
                crop_img = img.crop((left, upper, right, lower))
                crop_filename = f"crop_{session_timestamp}_r{row+1}_c{col+1}.jpg"
                crop_filepath = os.path.join(output_dir, crop_filename)
                crop_img.save(crop_filepath)
                cropped_mapping[f"{row+1}_{col+1}"] = crop_filename
        
        metadata = {
            "session_timestamp": session_timestamp,
            "full_image": full_image_filename,
            "grid": {
                "rows": rows,
                "columns": columns,
                "crop_square_size": crop_square_size,
                "x_padding": x_padding,
                "y_padding": y_padding
            },
            "cropped_images": cropped_mapping,
            "labels": common_labels or {}
        }
        
        metadata_filename = f"metadata_{session_timestamp}.json"
        with open(os.path.join(output_dir, metadata_filename), "w") as meta_file:
            json.dump(metadata, meta_file, indent=4)
    
    return metadata
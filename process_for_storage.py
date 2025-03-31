import glob
import os
import json
from datetime import datetime
from PIL import Image

def process_for_storage(full_image_path, cropping_settings, label_settings, output_dir):
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
    print("Processing image...::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::.")
    rows = int(cropping_settings.get("gridRows"))
    columns = int(cropping_settings.get("gridColumns"))
    crop_square_size = int(cropping_settings.get("cropSquareSize"))
    common_labels = label_settings

    # Extract passID and create passid_str (assumes label_settings contains "passID")
    passid = label_settings.get("passID")
    passid_str = f"{int(passid):04d}"
    
    # Look for matching metadata JSON file in output_dir using a glob search.
    metadata_files = glob.glob(os.path.join(output_dir, f"{passid_str}_*.json"))
    
    # Let's assume you expect only one metadata file per pass.
    if metadata_files:
        metadata_file = metadata_files[0]
        with open(metadata_file, "r") as f:
            stored_data = json.load(f)
        stored_labels = stored_data.get("labels", {})
        
        # Compare stored labels with the current label_settings (or common_labels)
        # Here we assume that the current label settings must match exactly.
        if stored_labels != label_settings:
            raise ValueError("Stored labels do not match the current label settings. Aborting process.")
 



    with Image.open(full_image_path) as img:
        width, height = img.size

        total_crop_width = columns * crop_square_size
        total_crop_height = rows * crop_square_size
        # Center the grid in the original image
        x_padding = max((width - total_crop_width) // 2, 0)
        y_padding = max((height - total_crop_height) // 2, 0)

        cropped_mapping = {}

        full_image_dir = os.path.join(output_dir,"image/")
        os.makedirs(full_image_dir, exist_ok=True)

        session_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Optionally, save the full image in the session folder
        full_image_filename = f"full_{session_timestamp}.jpg"
        img.save(os.path.join(full_image_dir, full_image_filename))

    if cropping_settings.get("CropEnable"):
            print("Cropping image...")
            for row in range(rows):
                for col in range(columns):
                    left = x_padding + col * crop_square_size
                    upper = y_padding + row * crop_square_size
                    right = left + crop_square_size
                    lower = upper + crop_square_size
                    
                    crop_img = img.crop((left, upper, right, lower))
                    crop_filename = f"crop_{session_timestamp}_r{row+1}_c{col+1}.jpg"

                    crop_image_dir = os.path.join(output_dir,"cropped/")
                    os.makedirs(crop_image_dir, exist_ok=True)
                    crop_filepath = os.path.join(crop_image_dir, crop_filename)
                    crop_img.save(crop_filepath)
                    cropped_mapping[f"{row+1}_{col+1}"] = crop_filename

    if label_settings.get("LabelEnable"):
        print("Adding labels...")
        print(common_labels)
        if cropping_settings.get("CropEnable"):
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
        else:
                        metadata = {
                "session_timestamp": session_timestamp,
                "full_image": full_image_filename,
                "labels": common_labels or {}
            }
        

        metadata_filename = f"metadata_{session_timestamp}.json"
        metadata_dir = os.path.join(output_dir,"metadata/")
        os.makedirs(metadata_dir, exist_ok=True)
        with open(os.path.join(metadata_dir, metadata_filename), "w") as meta_file:
            json.dump(metadata, meta_file, indent=4)
    
        return metadata
    return {}
    
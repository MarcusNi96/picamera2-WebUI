import glob
import os
import math
import json
from datetime import datetime

def create_pass(label_settings):
    passid = label_settings.get("passID")
    ra = label_settings.get("Ra")
    feed = label_settings.get("feed")
    depthOfCut = label_settings.get("depthOfCut")
    cuttingSpeed = label_settings.get("cuttingSpeed")
    insertRadius = label_settings.get("tipRadius")
    labelEnable = label_settings.get("LabelEnable")
    labelTurningEnable = label_settings.get("LabelTurningEnable")

    # Format passID as four digits, padded with zeros.
    passid_str = f"{int(passid):04d}"
    # Round to one decimal place for ra.
    ra_round = round(float(ra), 1)
    # Round to two decimal places for feed.
    feed_round = round(float(feed), 2)
    # Round to two decimal places for depthOfCut.
    depth_round = round(float(depthOfCut), 2)

    # Format cuttingSpeed and tipRadius normally with one decimal.
    cuttingSpeed_str = f"{float(cuttingSpeed):.1f}"
    insertRadius_str = f"{float(insertRadius):.1f}"

    # Build folder_name based on label settings.
    if not labelEnable or int(labelEnable) == 0:
        folder_name = f"{passid_str}"
    else:
        # When labelEnable is true, always append Ra
        folder_name = f"{passid_str}-Ra{ra_round:.1f}"
        # Additionally append the rest if labelTurningEnable is true.
        if labelTurningEnable and int(labelTurningEnable) != 0:
            folder_name = f"{folder_name}-f{feed_round:.2f}-a{depth_round:.2f}-v{cuttingSpeed_str}-RE{insertRadius_str}"

    base_dir = os.path.join("static", "gallery","data")
    dir = os.path.join(base_dir, folder_name)
    
    # Create directory and, if new and labelEnable is true, write the metadata file.
    if not os.path.exists(dir):
        # Check if any folder starting with passid_str already exists in base_dir.
        existing_folders = glob.glob(os.path.join(base_dir, f"{passid_str}*"))
        if existing_folders:
            raise ValueError(f"A folder with passID '{passid_str}' already exists. Aborting process.")
        
        os.makedirs(dir, exist_ok=True)
        if labelEnable and int(labelEnable) != 0:
            session_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            metadata = {
                "session_timestamp": session_timestamp,
                "labels": label_settings
            }
            metadata_path = os.path.join(dir, f"{passid_str}_{session_timestamp}.json")
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=4)
    else:
        os.makedirs(dir, exist_ok=True)
    
    print(dir)
    return dir
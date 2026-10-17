"""
preprocessing.py — One-time preprocessing pipeline.
Run this script once before running the research notebook.
Set the environment variable PROJECT_DIR to the folder that contains Data/.

Steps:
  1. Crop black padding from 80s NYC images
  2. Convert Roboflow polygon labels to YOLO bbox (80s and 90s)
  3. Convert Mapillary segmentation masks to YOLO
  4. Convert KITTI raw 15-value labels to YOLO format
  5. Merge converted KITTI labels with Roboflow building annotations
  6. Unify all datasets into unified_full/
"""

from utils import (
    crop_80s_dataset,
    convert_roboflow_labels,
    convert_mapillary_dataset,
    convert_kitti_raw_to_yolo,
    merge_kitti_labels,
    unify_dataset,
    UNIFIED_CLASSES,
)
import os
from pathlib import Path

BASE = Path(os.environ.get("PROJECT_DIR", ".")) / "Data"

# Step 1: Remove black padding from 80s NYC images
print("Step 1: Cropping 80s NYC images")
print("=" * 70)
crop_80s_dataset(
    source_images_dir = BASE / "Full_80s_data_roboflow" / "test" / "images",
    source_labels_dir = BASE / "Full_80s_data_roboflow" / "yolo_labels",
    output_dir        = BASE / "80s_cropped" / "80s",
    threshold         = 10,
    safety_margin     = 1,
)

# Step 2: Convert Roboflow labels → YOLO bbox (80s and 90s)
print("\nStep 2: Converting Roboflow labels to YOLO bbox format")
print("=" * 70)
convert_roboflow_labels(
    labels_dir = BASE / "Full_80s_data_roboflow" / "test" / "labels",
    output_dir = BASE / "Full_80s_data_roboflow" / "yolo_labels",
)
convert_roboflow_labels(
    labels_dir = BASE / "90s" / "valid" / "labels",
    output_dir = BASE / "90s" / "yolo_labels",
)

# Step 3: Convert Mapillary segmentation masks → YOLO
print("\nStep 3: Converting Mapillary masks to YOLO")
print("=" * 70)
convert_mapillary_dataset(
    masks_dir   = BASE / "Mapillary" / "Full_data",
    images_dir  = BASE / "Mapillary" / "Full_data",
    output_dir  = BASE / "Mapillary" / "Full_data" / "yolo_labels",
    config_path = BASE / "Mapillary" / "Full_data" / "config_v2.0.json",
    min_area    = 500,
)

import shutil

# Clean before Steps 4 and 5
for folder in [
    BASE / "KITTI" / "train" / "yolo_labels",
    BASE / "KITTI" / "merged_final",
    BASE / "unified_full" / "KITTI" / "labels",
]:
    if folder.exists():
        shutil.rmtree(folder)
        print(f"Cleaned: {folder}")

# Step 4: Convert KITTI raw 15-value labels → YOLO format
print("\nStep 4: Converting KITTI raw labels to YOLO format")
print("=" * 70)
convert_kitti_raw_to_yolo(
    raw_labels_dir = BASE / "KITTI" / "Sample_data_full" / "labels",
    images_dir     = BASE / "KITTI" / "Sample_data_full" / "images",
    output_dir     = BASE / "KITTI" / "train" / "yolo_labels",
)

# Step 5: Merge converted KITTI labels + Roboflow building annotations
# NOTE: converted_labels_dir is the OUTPUT of Step 4 (already YOLO format).
#       building_labels_dir is the original Roboflow polygon exports (.rf. files).
#       merge_kitti_labels converts the building polygons to bbox and appends them.
print("\nStep 5: Merging KITTI labels with building annotations")
print("=" * 70)
merge_kitti_labels(
    converted_labels_dir = BASE / "KITTI" / "train" / "yolo_labels",
    building_labels_dir  = BASE / "KITTI" / "train" / "labels",
    output_dir           = BASE / "KITTI" / "merged_final",
    clean_before_copy    = False,
    images_dir           = None,
)

# Step 6: Unify all datasets into unified_full/
print("\nStep 6: Unifying datasets")
print("=" * 70)

DATASETS = {
    "80s (NYC)": {
        "source_labels": BASE / "80s_cropped" / "80s" / "labels",
        "source_images": BASE / "80s_cropped" / "80s" / "images",
        "output"       : BASE / "unified_full" / "80s" / "labels",
        "img_ext"      : ".jpg",
        "remap"        : {0: 0, 1: 1, 2: 2, 3: 3, 4: 4},
    },
    "90s (LA/London)": {
        "source_labels": BASE / "90s" / "yolo_labels",
        "source_images": BASE / "90s" / "valid" / "images",
        "output"       : BASE / "unified_full" / "90s" / "labels",
        "img_ext"      : ".jpg",
        "remap"        : {0: 0, 1: 1, 2: 2, 3: 3, 4: 4},
    },
    "KITTI": {
        "source_labels": BASE / "KITTI" / "merged_final",
        "source_images": BASE / "KITTI" / "Sample_data_full" / "images",
        "output"       : BASE / "unified_full" / "KITTI" / "labels",
        "img_ext"      : ".png",
        "remap"        : {0: 0, 1: 1, 2: 2, 3: 3, 4: 4},
    },
    "Mapillary": {
        "source_labels": BASE / "Mapillary" / "Full_data" / "yolo_labels" / "labels",
        "source_images": BASE / "Mapillary" / "Full_data" / "yolo_labels" / "images",
        "output"       : BASE / "unified_full" / "Mapillary" / "labels",
        "img_ext"      : ".jpg",
        "remap"        : {0: 0, 1: 1, 2: 2, 3: 3, 4: 4},
    },
}

for name, cfg in DATASETS.items():
    str_cfg = {k: str(v) if isinstance(v, Path) else v for k, v in cfg.items()}
    unify_dataset(name, str_cfg, UNIFIED_CLASSES)

print("\n" + "=" * 70)
print("Preprocessing complete.")
print(f"Unified dataset: {BASE / 'unified_full'}")
print("Next: open notebooks/research_notebook.ipynb.")
print("=" * 70)
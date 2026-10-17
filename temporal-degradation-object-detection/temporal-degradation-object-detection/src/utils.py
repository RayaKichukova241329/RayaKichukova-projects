"""
utils.py — Preprocessing utilities for temporal degradation pipeline.

Covers:
  0. Roboflow label conversion (80s and 90s datasets)
  1. Mapillary segmentation mask → YOLO bounding box conversion
  2. 80s NYC black padding removal and coordinate adjustment
  3. KITTI raw format → YOLO conversion
  4. KITTI label merging (converted YOLO labels + building annotations)
  5. Dataset unification and class remapping to unified_full/
"""

import cv2
import numpy as np
import json
import shutil
from pathlib import Path
from tqdm import tqdm

UNIFIED_CLASSES = ['Building', 'Car', 'Truck', 'Pedestrian', 'Cyclist']

# Mapillary class mapping
MAPILLARY_REMAP = {
    'Building': 0,
    'Car': 1, "Bird's Eye Car": 1, 'Van': 1,
    'Truck': 2,
    'Person': 3, 'Person Group': 3,
    'Bicyclist': 4, 'Motorcyclist': 4, 'Other Rider': 4,
    'Bicycle': 4, 'Motorcycle': 4, 'Wheeled Slow': 4,
}

# KITTI class mapping
# Van merged into Car; DontCare, Misc, Tram, Person_sitting discarded
KITTI_NAME_TO_UNIFIED = {
    'Car': 1, 'Van': 1,
    'Truck': 2,
    'Pedestrian': 3,
    'Cyclist': 4,
}



# 0. ROBOFLOW LABEL CONVERSION (80s and 90s datasets)

def convert_roboflow_labels(labels_dir, output_dir):
    """
    Converts Roboflow-exported labels to YOLO bounding box format.
    Handles both polygon format and already-converted bbox format.
    Used for 80s NYC and 90s LA/London datasets.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    label_files = [f for f in Path(labels_dir).glob('*.txt')
                   if f.name != 'classes.txt']
    total_boxes = 0

    for lbl_path in tqdm(label_files, desc=f'Converting {Path(labels_dir).parent.name} labels'):
        bbox_lines = []
        for line in lbl_path.read_text().strip().splitlines():
            parts = line.strip().split()
            if len(parts) < 5:
                continue
            class_id = int(parts[0])
            coords = list(map(float, parts[1:]))

            if len(coords) == 4:
                cx, cy, w, h = coords
            else:
                x_coords = coords[0::2]
                y_coords = coords[1::2]
                if not x_coords or not y_coords:
                    continue
                x_min, x_max = min(x_coords), max(x_coords)
                y_min, y_max = min(y_coords), max(y_coords)
                cx = (x_min + x_max) / 2
                cy = (y_min + y_max) / 2
                w  = x_max - x_min
                h  = y_max - y_min

            if w > 0 and h > 0:
                bbox_lines.append(f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

        (out / lbl_path.name).write_text('\n'.join(bbox_lines))
        total_boxes += len(bbox_lines)

    (out / 'classes.txt').write_text('\n'.join(UNIFIED_CLASSES))
    print(f"Done. {len(label_files)} files → {total_boxes} bounding boxes.")



# 1. MAPILLARY: SEGMENTATION MASK → YOLO

def build_mapillary_color_map(config_path):
    """Builds color → unified_class_id lookup from Mapillary config_v2.0.json."""
    with open(config_path) as f:
        cfg = json.load(f)
    color_map = {}
    skipped = []
    for label in cfg['labels']:
        name = label['readable']
        r, g, b = label['color']
        if name in MAPILLARY_REMAP:
            color_map[(r, g, b)] = MAPILLARY_REMAP[name]
        else:
            skipped.append(name)
    return color_map, skipped


def mask_to_yolo(mask_path, output_dir, color_map, min_area=500, tolerance=1):
    """Converts a single Mapillary segmentation mask to a YOLO label file."""
    mask = cv2.imread(str(mask_path))
    if mask is None:
        return 0
    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
    h, w = mask_rgb.shape[:2]
    annotations = []

    for (r, g, b), class_id in color_map.items():
        lo = np.array([max(0, r-tolerance), max(0, g-tolerance), max(0, b-tolerance)])
        hi = np.array([min(255, r+tolerance), min(255, g+tolerance), min(255, b+tolerance)])
        binary = cv2.inRange(mask_rgb, lo, hi)
        if binary.sum() == 0:
            continue
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) < min_area:
                continue
            x, y, bw, bh = cv2.boundingRect(cnt)
            cx = (x + bw / 2) / w
            cy = (y + bh / 2) / h
            annotations.append(f"{class_id} {cx:.6f} {cy:.6f} {bw/w:.6f} {bh/h:.6f}")

    Path(output_dir).joinpath(f"{Path(mask_path).stem}.txt").write_text("\n".join(annotations))
    return len(annotations)


def convert_mapillary_dataset(masks_dir, images_dir, output_dir, config_path, min_area=500):
    """Batch converts all Mapillary masks to YOLO labels."""
    color_map, skipped = build_mapillary_color_map(config_path)
    print(f"Skipped {len(skipped)} Mapillary labels not in unified taxonomy.")

    out_labels = Path(output_dir) / 'labels'
    out_images = Path(output_dir) / 'images'
    out_labels.mkdir(parents=True, exist_ok=True)
    out_images.mkdir(parents=True, exist_ok=True)

    masks = sorted(Path(masks_dir).glob('*.png'))
    total_annotations = 0

    for mask_path in tqdm(masks, desc='Converting Mapillary masks'):
        n = mask_to_yolo(mask_path, out_labels, color_map, min_area)
        total_annotations += n
        for ext in ('.jpg', '.jpeg', '.png'):
            img = Path(images_dir) / (mask_path.stem + ext)
            if img.exists():
                shutil.copy(img, out_images / img.name)
                break

    print(f"Done. {len(masks)} masks → {total_annotations} annotations.")



# 2. 80s NYC: BLACK PADDING REMOVAL + COORDINATE ADJUSTMENT

def detect_content_bounds(image, threshold=10, safety_margin=1):
    """Detects bounding box of non-black content in an image."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = gray > threshold
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not rows.any() or not cols.any():
        return None
    y_idx = np.where(rows)[0]
    x_idx = np.where(cols)[0]
    x1 = max(0, x_idx[0] - safety_margin)
    y1 = max(0, y_idx[0] - safety_margin)
    x2 = min(image.shape[1] - 1, x_idx[-1] + safety_margin)
    y2 = min(image.shape[0] - 1, y_idx[-1] + safety_margin)
    return x1, y1, x2, y2


def adjust_yolo_labels(lines, old_w, old_h, crop_x, crop_y, new_w, new_h):
    """Re-normalizes YOLO coordinates after cropping."""
    adjusted = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 5:
            continue
        cid = int(parts[0])
        cx_n, cy_n, w_n, h_n = map(float, parts[1:5])
        new_cx = (cx_n * old_w - crop_x) / new_w
        new_cy = (cy_n * old_h - crop_y) / new_h
        new_w_n = (w_n * old_w) / new_w
        new_h_n = (h_n * old_h) / new_h
        if 0 <= new_cx <= 1 and 0 <= new_cy <= 1:
            adjusted.append(f"{cid} {new_cx:.6f} {new_cy:.6f} {new_w_n:.6f} {new_h_n:.6f}")
    return adjusted


def crop_80s_dataset(source_images_dir, source_labels_dir, output_dir,
                     threshold=10, safety_margin=1):
    """
    Removes black padding from all 80s NYC images and adjusts YOLO labels.
    Always crops to detected content bounds — no minimum padding threshold.
    """
    out_images = Path(output_dir) / 'images'
    out_labels = Path(output_dir) / 'labels'
    out_images.mkdir(parents=True, exist_ok=True)
    out_labels.mkdir(parents=True, exist_ok=True)

    images = sorted(Path(source_images_dir).glob('*.jpg'))
    skipped = 0

    for img_path in tqdm(images, desc='Cropping 80s images'):
        img = cv2.imread(str(img_path))
        if img is None:
            continue
        bounds = detect_content_bounds(img, threshold, safety_margin)
        if bounds is None:
            skipped += 1
            continue
        x1, y1, x2, y2 = bounds
        old_h, old_w = img.shape[:2]
        cropped = img[y1:y2+1, x1:x2+1]
        new_h, new_w = cropped.shape[:2]
        cv2.imwrite(str(out_images / img_path.name), cropped)
        label_path = Path(source_labels_dir) / f"{img_path.stem}.txt"
        if label_path.exists():
            lines = label_path.read_text().strip().splitlines()
            adjusted = adjust_yolo_labels(lines, old_w, old_h, x1, y1, new_w, new_h)
            (out_labels / label_path.name).write_text("\n".join(adjusted))
        else:
            (out_labels / f"{img_path.stem}.txt").write_text("")

    print(f"Done. {len(images) - skipped} images cropped, {skipped} skipped.")


# 3. KITTI: RAW FORMAT → YOLO CONVERSION

def convert_kitti_raw_label(kitti_line, img_w, img_h):
    """
    Converts a single KITTI raw annotation line to YOLO format.
    KITTI format: class truncated occluded alpha x1 y1 x2 y2 h w l X Y Z ry
    Returns YOLO string or None if class not in taxonomy.
    """
    parts = kitti_line.strip().split()
    if len(parts) < 9:
        return None
    class_name = parts[0]
    if class_name not in KITTI_NAME_TO_UNIFIED:
        return None
    class_id = KITTI_NAME_TO_UNIFIED[class_name]
    x1, y1, x2, y2 = float(parts[4]), float(parts[5]), float(parts[6]), float(parts[7])
    cx = ((x1 + x2) / 2) / img_w
    cy = ((y1 + y2) / 2) / img_h
    w  = (x2 - x1) / img_w
    h  = (y2 - y1) / img_h
    if w <= 0 or h <= 0:
        return None
    return f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}"


def convert_kitti_raw_to_yolo(raw_labels_dir, images_dir, output_dir):
    """
    Batch converts KITTI raw format labels to YOLO format.
    Input: 15-value KITTI text annotations.
    Output: normalised YOLO bbox annotations.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    label_files = sorted(Path(raw_labels_dir).glob('*.txt'))
    total_boxes = 0

    for lbl_path in tqdm(label_files, desc='Converting KITTI raw labels'):
        img_path = None
        for ext in ('.png', '.jpg', '.jpeg'):
            candidate = Path(images_dir) / (lbl_path.stem + ext)
            if candidate.exists():
                img_path = candidate
                break
        if img_path is None:
            continue
        img = cv2.imread(str(img_path))
        if img is None:
            continue
        img_h, img_w = img.shape[:2]
        yolo_lines = []
        for line in lbl_path.read_text().strip().splitlines():
            converted = convert_kitti_raw_label(line, img_w, img_h)
            if converted:
                yolo_lines.append(converted)
        (out / lbl_path.name).write_text('\n'.join(yolo_lines))
        total_boxes += len(yolo_lines)

    print(f"Done. {len(label_files)} KITTI files → {total_boxes} YOLO annotations.")


# 4. KITTI: MERGE CONVERTED YOLO LABELS + BUILDING ANNOTATIONS

def merge_kitti_labels(converted_labels_dir, building_labels_dir, output_dir,
                       clean_before_copy=True, images_dir=None):
    """
    Merges already-converted KITTI YOLO labels with Roboflow building annotations.

    converted_labels_dir : output of convert_kitti_raw_to_yolo (YOLO format)
    building_labels_dir  : Roboflow .rf. building annotation files
    output_dir           : destination for merged labels
    """
    import re

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    if clean_before_copy and images_dir is not None:
        dupes = list(Path(images_dir).glob('*.jpg'))
        png_stems = {p.stem for p in Path(images_dir).glob('*.png')}
        removed = sum(1 for jpg in dupes
                      if jpg.stem in png_stems and jpg.unlink() is None)
        if removed:
            print(f"Removed {removed} duplicate .jpg files.")

    # Index building files by leading numeric ID
    # e.g. "000026_png.rf.abc123.txt" → key "000026"
    building_dir = Path(building_labels_dir)
    building_index = {}
    for rf_file in building_dir.glob('*.txt'):
        if rf_file.name == 'classes.txt':
            continue
        match = re.match(r'^(\d+)', rf_file.stem)
        if match:
            building_index[match.group(1)] = rf_file

    converted_labels = sorted(Path(converted_labels_dir).glob('*.txt'))
    total_merged = 0

    for lbl in tqdm(converted_labels, desc='Merging KITTI labels'):
        # Read already-converted YOLO lines
        yolo_lines = [
            l.strip() for l in lbl.read_text().strip().splitlines() if l.strip()
        ]

        # Match building file by numeric ID
        numeric_id = re.match(r'^(\d+)', lbl.stem)
        building_file = building_index.get(numeric_id.group(1)) if numeric_id else None

        # Convert and append building annotations
        if building_file and building_file.exists():
            for line in building_file.read_text().strip().splitlines():
                parts = line.strip().split()
                if len(parts) < 5:
                    continue
                coords = list(map(float, parts[1:]))
                if len(coords) == 4:
                    cx, cy, w, h = coords
                else:
                    x_coords = coords[0::2]
                    y_coords = coords[1::2]
                    if not x_coords or not y_coords:
                        continue
                    cx = (min(x_coords) + max(x_coords)) / 2
                    cy = (min(y_coords) + max(y_coords)) / 2
                    w  = max(x_coords) - min(x_coords)
                    h  = max(y_coords) - min(y_coords)
                if w > 0 and h > 0:
                    yolo_lines.append(f"0 {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

        yolo_lines = list(dict.fromkeys(yolo_lines))
        (out / lbl.name).write_text("\n".join(yolo_lines))
        total_merged += 1

    print(f"Done. {total_merged} KITTI labels merged.")


# 5. UNIFICATION: REMAP AND COPY TO unified_full/

def unify_dataset(name, cfg, unified_classes=UNIFIED_CLASSES):
    """
    Applies class remapping and copies data into the unified_full/ structure.

    cfg keys:
        source_labels : path to source label directory
        source_images : path to source image directory
        output        : path to output labels directory
        img_ext       : image file extension e.g. '.jpg'
        remap         : {source_class_id: unified_class_id}
    """
    out_labels = Path(cfg['output'])
    out_images = out_labels.parent / 'images'
    out_labels.mkdir(parents=True, exist_ok=True)
    out_images.mkdir(parents=True, exist_ok=True)

    label_files = sorted(Path(cfg['source_labels']).glob('*.txt'))
    copied_labels = 0

    for lbl in label_files:
        if lbl.name == 'classes.txt':
            continue
        new_lines = []
        for line in lbl.read_text().strip().splitlines():
            parts = line.strip().split()
            if not parts:
                continue
            new_cid = cfg['remap'].get(int(parts[0]))
            if new_cid is not None:
                new_lines.append(f"{new_cid} " + " ".join(parts[1:]))
        (out_labels / lbl.name).write_text("\n".join(new_lines))
        copied_labels += 1

    copied_images = 0
    for img in Path(cfg['source_images']).glob(f"*{cfg['img_ext']}"):
        shutil.copy(img, out_images / img.name)
        copied_images += 1

    (out_labels / 'classes.txt').write_text("\n".join(unified_classes))
    print(f"{name}: {copied_labels} labels, {copied_images} images unified.")
from PIL import Image
from tqdm import tqdm
import pillow_avif
import os


def save_avif(path, img):
    """
    where quality is from 0-100 and speed is from 0-10
    quality 0 means bad quality 100 best lossless like
    speed 0 means slowest speed, best compresion.
    speed 10 means fastest and worst compression
    """

    avif_path = os.path.splitext(path)[0] + ".avif"
    img.save(avif_path, "AVIF", quality=80, speed=6)
    return avif_path


def delete_img_after_encode(path):
    os.remove(path)


def process_images_in_folder(start_folder):
    images_to_process = []

    for dirpath, _, filenames in os.walk(start_folder):
        for filename in filenames:
            if not filename.lower().endswith('.avif'):
                full_path = os.path.join(dirpath, filename)
                images_to_process.append(full_path)

    for full_path in tqdm(images_to_process, desc="Processing images"):
        try:
            # Load the image
            img = Image.open(full_path)
            # Convert and save in AVIF format
            save_avif(full_path, img)
            # Delete the original image
            delete_img_after_encode(full_path)
        except Exception as e:
            print(f"Failed processing {full_path}. Error: {e}")


def get_folder_size(path):
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total += os.path.getsize(fp)
    # in bytes
    return total


def calculate_size_reduction(old_size, new_size):
    reduction = old_size - new_size
    percentage_reduction = (reduction / old_size) * 100 if old_size > 0 else 0
    return reduction, percentage_reduction

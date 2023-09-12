from PIL import Image
from tqdm import tqdm
import pillow_avif
import os
import time
import subprocess

def save_avif(path, img):
    avif_path = os.path.splitext(path)[0] + ".avif"
    img.save(avif_path, "AVIF", quality=80, speed=0)
    return avif_path

def get_file_size(path):
    return os.path.getsize(path)

start_time = time.time()
img = Image.open("a.png")
save_avif("a.png", img)
pillow_time = time.time() - start_time

start_time = time.time()
subprocess.run(["convert", "a.png", "define", "heic:speed=2", "-quality", "80", "c.avif"])
command_time = time.time() - start_time

print(f"Conversion time using Pillow: {pillow_time} seconds")
print(f"Conversion time using command: {command_time} seconds")

print(f"File size of a.png: {get_file_size('a.png')} bytes")
print(f"File size of a.avif: {get_file_size('a.avif')} bytes")
print(f"File size of c.avif: {get_file_size('c.avif')} bytes")

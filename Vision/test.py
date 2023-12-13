from PIL import Image
import numpy as np
import os
import json
import cv2


png_files = [f for f in os.listdir('.\\masks') if f.endswith('.npy')]
pg = [f for f in os.listdir('.\\') if f.endswith('.png')]
for p in pg:
    mask = np.load(".\\masks\\"+p[:-4]+".npy")
    i = Image.open(p)
    i = i.convert('RGB')
    image_array = np.array(i)
    mask = mask
    c = np.multiply(image_array, np.repeat(mask[:,:,np.newaxis],3,axis=2))
    im = Image.fromarray(c, mode='RGB')
    im.save(p)


# f = open('meta_data.json', 'r')
# meta_data = json.load(f)
# meta_data["has_foreground_mask"] = True
# for f in meta_data["frames"]:
#     f["mask_path"] = "masks/"+f["rgb_path"][:-4]+".jpeg"

# c = open('meta_data_new.json', 'w')
# json.dump(meta_data, c)
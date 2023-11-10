from pylab import imshow
import numpy as np
import cv2
import torch, json
import albumentations as albu
from iglovikov_helper_functions.utils.image_utils import load_rgb, pad, unpad
from iglovikov_helper_functions.dl.pytorch.utils import tensor_from_rgb_image
from people_segmentation.pre_trained_models import create_model

model = create_model("Unet_2020-07-20")
model.eval()

def create_mask(image_path):
    image = load_rgb(image_path)
    transform = albu.Compose([albu.Normalize(p=1)], p=1)
    padded_image, pads = pad(image, factor=32, border=cv2.BORDER_CONSTANT)
    x = transform(image=padded_image)["image"]
    x = torch.unsqueeze(tensor_from_rgb_image(x), 0)
    with torch.no_grad():
        prediction = model(x)[0][0]
    mask = (prediction > 0).cpu().numpy().astype(np.uint8)
    mask = unpad(mask, pads)

    if image_path[-5:] == ".jpeg":
        np.save("masks/"+image_path[:-5])
        return "masks/"+image_path[:-5]+".npy"
    elif image_path[-4:] == ".png":
        np.save("masks/"+image_path[:-4])
        return "masks/"+image_path[:-4]+".npy"
    


meta_data = json.load("meta_data.json")
meta_data["has_foreground_mask"] = True
for f in meta_data["frames"]:
    f["mask_path"] = create_mask(f["rgb_path"])

json.dumps(meta_data, "meta_data_new.json")
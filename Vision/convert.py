from PIL import Image
import pillow_heif
from os import listdir
from os.path import isfile, join
# path = r'.\data\scan'
path = '.'
onlyfiles = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

i = 0
for f in onlyfiles:
    heif_file = pillow_heif.read_heif(f)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",

    )

    image.save("./output/t"+str(i)+".png", format("png"))
    i += 1
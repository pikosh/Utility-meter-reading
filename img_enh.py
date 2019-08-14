from PIL import Image, ImageEnhance
import os

def img_enh(fpath):
    for dirpath, _, filenames in os.walk(fpath):
        for fl in filenames:
            img = Image.open(os.path.join(dirpath, fl))
            img = img.resize((28, 28))
            # img = img.convert('L')
            enhancer = ImageEnhance.Contrast(img)
            enhanced_im = enhancer.enhance(5.0)
            #try to change 5
            enhanced_im.save(os.path.join(dirpath, fl))
#, Image.ANTIALIAS
if __name__ == '__main__':
    img_enh('/home/perizat/Рабочий стол/thesis/data set/digits_borders')
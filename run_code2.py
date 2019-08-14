import sys
import os
import glob
import json
import numpy as np
import cv2
# from parser3 import xmlparser
from measure_image2 import measure_image2
# from interOverUnion2 import RotatedRect


def get_all_images(folder):
    dictio_i1 = dict()
    dictio_i2 = dict()
    for dirpath, _, filenames in os.walk(folder):
        for fl in filenames:
            img_name1 = os.path.splitext(fl)[0]
            (cx, cy, w, h, angle)=measure_image2(os.path.join(dirpath, fl))
            #algorithm1: cx = w, cy = (y + h)*0.9, w = ((x + w1)/2)*1.3, h is original
            cy1 = int((cy + h)*0.9)
            w = int(((cx + w)/2)*1.5)
            cx = int(w*0.8)
            h1 = int(h*1.5)
            #algorithm2: cx = w, cy = (y + h)*0.8, w = ((x + w1)/2)*1.3, h is original
            cy2 = (cy + h)*0.85
            dictio_i1.update({img_name1 : (cx, cy1, w, h1, angle)})
            dictio_i2.update({img_name1 : (cx, cy2, w, h1, angle)})
        return dictio_i1, dictio_i2

def crop_imgs(dictio, fpath):
    path1 = '/home/perizat/Рабочий стол/thesis/data set/test'
    # contours = get_contours(img)
    # boxes = get_windows(contours)
    # boxes2 = add_box(boxes)
    for dirpath, _, filenames in os.walk(fpath):
        for fl in filenames:
            img = cv2.imread(os.path.join(dirpath, fl))
            img_name = os.path.splitext(fl)[0]
            for key in dictio:
                values = dictio[key]
                x, y, w, h, _ = values
                x, y, w, h = int(round(x-w/2)), int(round(y-h/2)), int(w), int(h)
                if key == img_name:
                    res = cv2.putText(img, "Red contour bound", (x+w, y+h), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, lineType=cv2.LINE_AA)
                    xs = img[y:y+h, x:x+w]
            cv2.imwrite(os.path.join(path1, ( (img_name + '_%d' % 1) + '.png')), res)

"""def get_all_annotations(folder2):
    dictio_a = dict()
    for dirpath, _, filenames in os.walk(folder2):
        for fl in filenames:
            img_name2 = os.path.splitext(fl)[0]
            (cx, cy, w, h, angle) = xmlparser(os.path.join(dirpath, fl))            
            dictio_a.update({img_name2 : (cx, cy, w, h, angle)})
        return dictio_a


def get_all_IoU(dictio_i, dictio_a):
    dictio_results = dict()
    for key in dictio_i:
        value1 = dictio_i[key]
        r1 = RotatedRect(*value1)
        for key2 in dictio_a:
            value2 = dictio_a[key2]
            r2 = RotatedRect(*value2)
            if key == key2:                
                result = r1.intersection(r2).area / r1.union(r2).area
                dictio_results.update({key:result})
    return dictio_results

def mean_variance(dictio_results):
    variables = list()
    variance_mean = dict()
    for key in dictio_results:
        value = dictio_results[key]
        variables.append(value)
    variance = np.var(variables)
    mean = np.mean(variables)
    variance_mean.update({"variance" : variance, "mean" : mean})
    return variance_mean


def write_result(dictio_results1, dictio_results2, variance_mean1, variance_mean2):
    with open ("results_IoU2.json", "w") as f:
        json.dump("algorithm 1", f)
        json.dump(dictio_results1, f,indent=2)
        json.dump(variance_mean1, f, indent=4)
        json.dump("algorithm 2", f)
        json.dump(dictio_results2, f,indent=2)
        json.dump(variance_mean2, f, indent=4)
    return f

def write_result_imgs1(dictio_i1):
    with open ("results_imgs1.json", "w") as i:
        json.dump(dictio_i1, i,indent=2)
    return i

def write_result_anns(dictio_a):
    with open ("results_anns.json", "w") as i:
        json.dump(dictio_a, i,indent=2)
    return i

def write_result_imgs2(dictio_i2):
    with open ("results_imgs2.json", "w") as i:
        json.dump(dictio_i2, i,indent=2)
    return i"""


if __name__ == "__main__":
    # dictio_a = get_all_annotations('/home/perizat/Рабочий стол/thesis/current work/resized_img anns')'/home/perizat/Рабочий стол/thesis/data set/resized'
    dictio_i1, dictio_i2 = get_all_images('/home/perizat/Рабочий стол/thesis/rectangles/rectangle3')
    # dictio_i1, dictio_i2 = get_all_images('/home/perizat/Рабочий стол/thesis/current work/resized imgs')
    # dictio_results1 = get_all_IoU(dictio_i1, dictio_a)
    # dictio_results2 = get_all_IoU(dictio_i2, dictio_a)
    # variance_mean1 = mean_variance(dictio_results1)
    # variance_mean2 = mean_variance(dictio_results2)
    # write_result(dictio_results1, dictio_results2, variance_mean1, variance_mean2)
    crop_imgs(dictio_i2, '/home/perizat/Рабочий стол/thesis/rectangles/rectangle3')
    # write_result_imgs1(dictio_i1)
    # write_result_anns(dictio_a)
    # write_result_imgs2(dictio_i2)
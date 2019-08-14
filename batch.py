import cv2
import numpy as np
import matplotlib.pyplot as plt
import pathlib
import os


class OCRError(Exception):
    pass


def get_contours(img):
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #edges = cv2.Canny(img, 235, 250, apertureSize=3, L2gradient=True)
    edges = cv2.Canny(img, 150, 250, apertureSize=3, L2gradient=True)
    _, contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #images, contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return filter_(contours)


def filter_(contours):
    contours_dict = dict()
    for cont in contours:
        x, y, w, h = cv2.boundingRect(cont)
        area = cv2.contourArea(cont)
        #if 8 < area and 8 < w and 45 > w and h > 5:
        if 8 < area and 8 < w and 45 > w and h > 15 and 50 > h:
            contours_dict[(x, y, w, h)] = cont
    return sorted(contours_dict.values(), key=cv2.boundingRect)


def to_contours_image(contours, ref_image):
    blank_background = np.zeros_like(ref_image)
    img_contours = cv2.drawContours(blank_background, contours, -1, (255, 255, 255), thickness=2)
    #cv2.imwrite("img_contours.png", img_contours)
    return img_contours


def is_overlapping_horizontally(box1, box2):
    x1, _, w1, _ = box1
    x2, _, _, _ = box2
    if x1 > x2:
        return is_overlapping_horizontally(box2, box1)
    return (x2 - x1) < w1


def merge(box1, box2):
    assert is_overlapping_horizontally(box1, box2)
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    x = min(x1, x2)
    w = max(x1 + w1, x2 + w2) - x
    y = min(y1, y2)
    h = max(y1 + h1, y2 + h2) - y
    return x, y, w, h


def get_windows(contours):
    """return List[Tuple[x: Int, y: Int, w: Int, h: Int]]"""
    boxes = []
    for cont in contours:
        box = cv2.boundingRect(cont)
        if not boxes:
            boxes.append(box)
        else:
            if is_overlapping_horizontally(boxes[-1], box):
                last_box = boxes.pop()
                merged_box = merge(box, last_box)
                boxes.append(merged_box)
            else:
                boxes.append(box)
    return boxes

def add_box(boxes):
    dist, xs, ys, ws, hs = [], [], [], [], []
    for box in boxes:
        for i in range(0, len(box)):
            if i == 0:
                xs.append(box[i])
            elif i == 1:
                ys.append(box[i])
            elif i == 2:
                ws.append(box[i])
            elif i == 3:
                hs.append(box[i])
    mid_w, mid_h = ws[int(len(ws)/2)], hs[int(len(hs)/2)]
    for i, _ in enumerate(xs):
        d = (xs[i] - xs[i-1])
        dist.append(d)
    dist.pop(0)
    print(dist)
    mid_dist = dist[int(len(dist)/2)]
    mid_dist = int(mid_dist*0.98)
        
    for i, d in enumerate(dist):
        new_cx = xs[i]+mid_dist
        new_cx2 = new_cx + mid_dist
        new_cy = int((ys[i]+ys[i+1])/2)
        if d >= mid_dist*1.3 and d <= mid_dist*2.3:
            boxes.append((new_cx, new_cy, mid_w, mid_h))
        elif d >= mid_dist*2.4 and d <= mid_dist*3.3:
            boxes.append((new_cx, new_cy, mid_w, mid_h))
            boxes.append((new_cx2, new_cy, mid_w, mid_h))
    return boxes

def to_digit_images(img):
    contours = get_contours(img)
    # image_contours = to_contours_image(contours, img)
    windows = get_windows(contours)
    boxes = add_box(windows)
    #print(len(windows))
    if len(boxes) < 1:
        raise OCRError
    #extended bounds
    boxes_extend = []
    for box in boxes:
        x1, y1, w1, h1 = box
        x, y, w, h, = x1-5, y1-5, w1+8, h1+8
        boxes_extend.append((x, y, w, h))
    xs = [img[y:y+h, x:x+w] for (x, y, w, h) in boxes_extend]
    #ends here
    # xs = [img[y:y+h, x:x+w] for (x, y, w, h) in boxes]
    # xs = cv2.resize(xs, (28, 28))
    return xs

def draw_cont (fpath):
    img = cv2.imread(fpath.as_posix())
    path3 = '/home/perizat/Рабочий стол/thesis/data set/windows9'
    contours = get_contours(img)
    boxes = get_windows(contours)
    boxes2 = add_box(boxes)
    for box in boxes2:
        x, y, w, h = box
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite(os.path.join(path3, (fpath.stem + '_box' + '.png')), img)

def file2files(fpath):
    img = cv2.imread(fpath.as_posix(), cv2.IMREAD_GRAYSCALE)
    path1 = '/home/perizat/Рабочий стол/thesis/train network/single resized digits'
    # cv2.imwrite(os.path.join(path5, (fpath.stem + '.png')), edges)
    rois = to_digit_images(img)
    for i, digit_img in enumerate(rois):
        cv2.imwrite(os.path.join(path1, (fpath.stem + ('_%d' % i) + '.png')), digit_img)
        

def batch(data_dir='/home/perizat/Рабочий стол/thesis/train network/cropped resized images'):
    p = pathlib.Path(data_dir)
    paths = p.glob('*.png')
    for fpath in paths:
        print('  ...processing', fpath.name)
        try:
            file2files(fpath)
            # draw_cont (fpath)
        except OCRError:
            print('     [OCR ERROR]', fpath)
            continue


if __name__ == '__main__':
    batch()

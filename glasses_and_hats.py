import cv2
import os
import face_recognition as fr
import phrase2action
from PIL import Image

def load_resources(path):
    files = os.listdir(path)
    templates = []
    for file_path in files:
        if '.png' in file_path:
            relative_path = os.path.join(path, file_path)
            templates.append(cv2.imread(relative_path, -1))
            #print (templates[-1].shape)
    return templates

def add_glasses(img, glasses, rate, cnt):
    face_cascade = cv2.CascadeClassifier('/home/york_io/.local/lib/python3.6/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('/home/york_io/.local/lib/python3.6/site-packages/cv2/data/haarcascade_eye.xml')
    face_locs = []
    face_locs = []
    hat_locs = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_locs = face_cascade.detectMultiScale(gray, 1.3, 5)
    for loc in face_locs:
        x, y, w, h = loc
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if (len(eyes) < 2):
            continue
        expected_y = h // 3
        best_y = 123456789
        for eye in eyes:
            if abs(y - expected_y) < abs(best_y - expected_y):
                best_y = eye[1]
        gw = int(w * 0.9)
        delta = (w - gw) // 2
        #print(glasses.shape)
        gh = int(gw / glasses.shape[1] * glasses.shape[0])
        gx = x + delta
        gy = y + expected_y - int(0.15 * gh)
        if gx < 0 or gy < 0:
            continue
        glass_img = cv2.resize(glasses, (gw, gh))
        for yi in range(gy, gy + gh):
            for xi in range(gx, gx + gw):
                if glass_img[yi - gy, xi - gx, 3] != 0:
                    img[yi, xi] = glass_img[yi - gy, xi - gx, 0:3]
    return face_locs, hat_locs, img

def add_hat(img, hat_templ, rate, cnt):
    face_cascade = cv2.CascadeClassifier('/home/york_io/.local/lib/python3.6/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    face_locs = []
    hat_locs = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_locs = face_cascade.detectMultiScale(gray, 1.3, 5)
    for loc in face_locs:
        width_scaled = loc[2]
        width_original = hat_templ.shape[1]
        scale_factor = width_scaled / width_original
        estimated_height = int(hat_templ.shape[0] * scale_factor)
        delta = int(0.1 * estimated_height)
        x, y, w, h = loc
        hat_locs.append([y - estimated_height + delta, x + w, y + delta, x])
    for loc in face_locs:
        x, y, w, h = loc
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
    for hat_loc in hat_locs:
        if hat_loc[0] < 0:
            continue
        t, r, b, l = hat_loc
        w = r - l
        h = b - t
        hat_img = cv2.resize(hat_templ, (w, h))
        for y in range(t, b):
            for x in range(l, r):
                if hat_img[y - t, x - l, 3] != 0:
                    img[y, x] = hat_img[y - t, x - l, 0:3]
    return face_locs, hat_locs, img


def show_webcam(templ, process, rate = 5):
    cam = cv2.VideoCapture(0)
    cnt = 0
    face_locs = []
    while True:
        ret_val, img = cam.read()
        face_locs, obj_locs, img = process(img, templ, rate, cnt)
        cv2.imshow('my webcam', img)
        # right arrow == "YES"
        key = cv2.waitKey(1)
        #print(key)
        if key == 83:
            cv2.destroyAllWindows()
            return phrase2action.Actions.Y
        # left arrow == "NO"
        if key == 81:
            cv2.destroyAllWindows()
            return phrase2action.Actions.N
    cv2.destroyAllWindows()
    return phrase2action.Actions.N


def main():
    hat_templ = load_resources('hat_resources')
    glass_templ = load_resources('glass_resources')
    for t in glass_templ:
        show_webcam(t, add_glasses, rate=3)


if __name__ == '__main__':
    main()

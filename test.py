import cv2
import os
import face_recognition as fr
from PIL import Image

def load_resources(path='resources'):
    files = os.listdir(path)
    templates = []
    for file_path in files:
        if '.png' in file_path:
            relative_path = os.path.join(path, file_path)
            templates.append(cv2.imread(relative_path, -1))
            print (templates[-1].shape)
    return templates

def show_webcam(templ, rate = 5):
    cam = cv2.VideoCapture(0)
    cnt = 0
    face_locs = []
    hat_locs = []
    while True:
        ret_val, img = cam.read()
        if (cnt % rate == 0):
            hat_locs = []
            face_locs = fr.face_locations(img)
            for locs in face_locs:
                width_scaled = locs[1] - locs[3]
                width_original = templ.shape[1]
                scale_factor = width_scaled / width_original
                estimated_height = int(templ.shape[0] * scale_factor)
                delta = int(0.1 * estimated_height)
                hat_locs.append([locs[0] - estimated_height + delta, locs[1], locs[0] + delta, locs[3]])
        for loc in face_locs:
            t, r, b, l = loc
            cv2.rectangle(img, (l, t), (r, b), (0, 255, 0), 3)
        for hat in hat_locs:
            if hat[0] < 0:
                continue
            t, r, b, l = hat
            w = r - l
            h = b - t
            hat_img = cv2.resize(templ, (w, h))
            for y in range(t, b):
                for x in range(l, r):
                    #dec_threshold = hat_img[y - t, x - l][0] + hat_img[y - t, x - l][1] + hat_img[y - t, x - l][2]
                    #if dec_threshold < 245 * 3 and dec_threshold > 15:
                    if hat_img[y - t, x - l, 3] != 0:    
                        img[y, x] = hat_img[y - t, x - l, 0:3]
        
        cv2.imshow('my webcam', img)
        print(img.shape)
        

        if cv2.waitKey(1) == 27: 
            break  # esc to quit
        cnt += 1
    cv2.destroyAllWindows()


def main():
    templ = load_resources()
    for t in templ:
        show_webcam(templ = t, rate=3)


if __name__ == '__main__':
    main()

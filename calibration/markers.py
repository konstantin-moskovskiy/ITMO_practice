import cv2
import numpy as np
import cv2.aruco as aruco
import os
from PIL import Image


aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

images = []



folder_path = 'img'
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image = cv2.imread(os.path.join(folder_path, filename))
        width = int(image.shape[1] * 80 / 100)
        height = int(image.shape[0] * 80 / 100)
        dim = (width, height)
        image = cv2.resize(image, dim, interpolation= cv2.INTER_AREA)
        images.append(image)

resulted_images = []
sum_weight = 0
id_prev = []
dict_prev = {}

for number, image in enumerate(images):
    if number > 0:
        corners, ids, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters=parameters)
        dict_c = {}
        if len(corners) > 0:
            for i in range(len(corners)):
                corner = corners[i][0]
                x, y, w, h = cv2.boundingRect(corner)
                dict_c[ids[i][0]] = [x, y]
        id_c = [x[0] for x in ids]
        id_c.sort()

        A = np.array([dict_prev[id_prev[1]], dict_prev[id_prev[2]], dict_prev[id_prev[3]]]).astype(np.float32)
        #print(f"{A=}")
        B = np.array([dict_c[id_c[1]], dict_c[id_c[2]], dict_c[id_c[3]]]).astype(np.float32)
        #print(f"{B=}")
        warp_mat = cv2.getAffineTransform(B, A)
        warp_dst = cv2.warpAffine(image, warp_mat, (image.shape[1], image.shape[0]))
        gran = 1024 - (dict_prev[1+4*number][0] + (1024 - dict_c[1+4*number][0]))

        dict_prev = {}
        corners, ids, _ = cv2.aruco.detectMarkers(warp_dst, aruco_dict, parameters=parameters)
        if len(corners) > 0:
            for i in range(len(corners)):
                corner = corners[i][0]
                x, y, w, h = cv2.boundingRect(corner)
                dict_prev[ids[i][0]] = [x, y]
        id_prev = [x[0] for x in ids]
        id_prev.sort()
        print(f"{number=}")
        print(f"{dict_prev=}")
        print(f"{id_prev=}")
        cv2.imshow(f"map{number}", warp_dst)
        warp_dst = warp_dst[:, :gran, :]
        warp_dst_2 = Image.fromarray(warp_dst)
        bbox = warp_dst_2.getbbox()
        warp_dst = warp_dst[:, bbox[0]+10:, :]
        # warp_dst = warp_dst.crop(bbox)
        # warp_dst = np.array(warp_dst)

        resulted_images.append(warp_dst)
        sum_weight += warp_dst.shape[1]
        #cv2.imshow(f"map{number}", warp_dst)
        # print(warp_mat)
    else:
        corners, ids, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters=parameters)
        if len(corners) > 0:
            for i in range(len(corners)):
                corner = corners[i][0]
                x, y, w, h = cv2.boundingRect(corner)
                dict_prev[ids[i][0]] = [x, y]
        id_prev = [x[0] for x in ids]
        id_prev.sort()
        resulted_images.append(image)
        sum_weight += image.shape[1]
        sum_height = image.shape[0]
        print(f"{number=}")
        print(f"{dict_prev=}")
        print(f"{id_prev=}")

resulted_images.reverse()
resulted_image = Image.new("RGB", (sum_weight, sum_height))

resulted_image.paste(Image.fromarray(resulted_images[0]), (0, 0))
resulted_image.paste(Image.fromarray(resulted_images[1]), (resulted_images[0].shape[1], 0))
resulted_image.paste(Image.fromarray(resulted_images[2]), (resulted_images[0].shape[1] + resulted_images[1].shape[1], 0))
resulted_image.save("result.jpg")
#cv2.imshow('Result', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
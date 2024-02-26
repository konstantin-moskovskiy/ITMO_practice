
import uuid
import cv2
import numpy as np
import time
from connector import *

my_block_id = '10.8.130.20'
gr_UUID = str(uuid.uuid4())
def get_image_size(image_path):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    return width, height

def get_numpy_image(image_path):
    image = cv2.imread(image_path)
    return np.array(image)


def create_image_packet(image_type, image_path, map_data, image):

    width, height = get_image_size(image_path)

    header = {
        "version": "0.7",
        "uuid": str(uuid.uuid4()),
        "timestamp": int(time.time()),
        "packet": image_type,
        "groupUUID": gr_UUID,  # Генерация уникального UUID для группы пакетов (если нужно)
        "packetNumber": 1,  # Номер пакета (здесь 1, так как один пакет)
        "totalPackages": 1,  # Всего пакетов в группе (здесь 1, так как один пакет)
        "consume_queue": "calculator.output.img",
        "block_id": my_block_id
    }

    image_metadata = {
        "calculatorSheetID": "1",
        "innerSheetID": "1",
        "isFinal": False,
        "type": image_type,
        "height": {"px": height},
        "width": {"px:": width},
        "cameraNumber": 2,
        "coordinates": {"x_px": 0, "y_px": 0, "x_mm": 1.0, "y_mm": 1.0},
        "imgMapArray": image
    }

    packet = {
        "header": header,
        "body": {
            "images": [image_metadata]
        }
    }

    return packet


stitching_metadata = {
    "type": "stitching",
    "img": "1.bmp",
    "map_inf": {"key1": "value1", "key2": "value2"},
}

projection_metadata = {
    "type": "projection",
    "img": "2.bmp",
    "map_inf": {"key1": "value1", "key2": "value2"},
}

deepmap2D_metadata = {
    "type": "deepmap2D",
    "img": "3.bmp",
    "map_inf": {"key1": "value1", "key2": "value2"},
}


stitching_packet = create_image_packet("stitching", stitching_metadata["img"], stitching_metadata["map_inf"], get_numpy_image(stitching_metadata["img"]))
projection_packet = create_image_packet("projection", projection_metadata["img"], projection_metadata["map_inf"], get_numpy_image(projection_metadata["img"]))
deepmap2D_packet = create_image_packet("deepmap2D", deepmap2D_metadata["img"], deepmap2D_metadata["map_inf"], get_numpy_image(deepmap2D_metadata["img"]))


try:
    r = RedisClient(host='192.168.0.101', port=6379, stream='data_from_itmo')
    r.push_data(stitching_packet)
    r.push_data(projection_packet)
    r.push_data(deepmap2D_packet)
    print("JSON-пакеты успешно отправлены в Redis.")
except Exception as e:
    print(f"Ошибка при отправке в Redis: {str(e)}")


import json
import time
import uuid
from ximea import xiapi
from error_codes import ERROR_CODES
from connector import *

my_block_id = '10.8.130.22'
# to Redis
def send_camera_status_to_redis(camera_status):
    r = RedisClient(host='192.168.0.101', port=6379, stream="camera_status")
    r.push_data(json.dumps(camera_status))
    print(f"Статус с блока {my_block_id} был отправлен на сервер")


def get_camera_status():
    cam = xiapi.Camera()
    cam.open_device()
    img = xiapi.Image()

    try:
        # Проверка состояния камеры.
        # Если статус доступности камеры успешен, устанавливаем status=1
        # Если камера недоступна, status=0, и в errors добавить описание проблемы.
        #cam.get_image(img) #проверка по получение изображения
        cam.set_exposure(10000)  # установка выдержки
        #temp = cam.get_temp()

        status = 1  
        errors = []

    except xiapi.Xi_error as e:
        status = 0
        error_code = e.status  # код ошибки
        error_message = ERROR_CODES.get(error_code)  # описание ошибки из xidefs.py #ERROR_CODES
        errors = [f"Error Code: {error_code}, Message: {error_message}"]
        

    finally:
        cam.close_device()  

    return status, errors

def send_camera_status():
    new_uuid = str(uuid.uuid4())
    #status, errors = get_camera_status()
    status, errors = 1, ['None']


    camera_status = {
        "header": {
            "version": "0.2",
            "uuid": new_uuid,  
            "timestamp": int(time.time()),  
            "packet": "healthcheckOutputCalculator",
            "consume_queue": "calculator.output.healthcheck",
            "block_id": my_block_id
        },
        "body": {
            "cameras": [
                {
                    "name": "XIMEA Camera",  # Наименование камеры
                    "position": 1,  # Порядковый номер камеры
                    "status": status,  # Полученный статус
                    "errors": errors  # Описание проблем при статусе 0 (если есть)
                }
            ]
        }
    }

    send_camera_status_to_redis(camera_status)

while True:
    send_camera_status()
    time.sleep(30)  # Задержка в X секунд

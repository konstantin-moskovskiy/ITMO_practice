import redis
from pydantic import ValidationError
import json
from json import JSONEncoder
import numpy
from schemas import JSON1, JSON0, JSON3, JSON31, JSON32, \
     JSON4, JSON5, JSON2, Data, Data2, DataCamera, JSON6, GeometryEvaluation
import logging

stream_schemas = {
    "data_from_itmo": Data,
    "data_for_itmo": Data2,
    "camera_status": DataCamera,
    "start_calibration": JSON1,
    "selecting_camera_side": JSON0,
    "img_for_evaluation": JSON3,
    "calibration_confirmation": JSON31,
    "converted_image": JSON32,
    "camera_to_server": JSON2,
    "server_to_camera": JSON4,
    "confirm_matrix_application": JSON5,
    "calibration_finalization": JSON6,
    "geometry_evaluation": GeometryEvaluation
}

logging.basicConfig(level=logging.INFO, filename="redis.log", filemode="w")

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

class RedisClient:
    def __init__(self, host='localhost', port=6379, stream=None):
        if stream not in stream_schemas.keys():
            raise Exception(f"invalid thread name. must be in {list(stream_schemas.keys())}")

        self.r = redis.Redis(host=host, port=port)
        self.stream = stream
        self.schema = stream_schemas[stream]

    def _check_valid(self, item):
        # проверка валидности json
        if isinstance(item, bytes):
            item = item.decode("utf-8").replace('\'', '\"')
        if isinstance(item, str):
            try:
                json_item = json.loads(item)
            except json.JSONDecodeError as exc:
                logging.error(f"invalid JSON: {exc.msg}, line {exc.lineno}, column {exc.colno}")
                return False
        elif isinstance(item, dict):
            json_item = item
        else:
            logging.error("data must be json or dict")
            return False
        # проверка соответствия схеме данных
        try:
            self.schema(**json_item)
            return json_item
        except ValidationError as exc:
            logging.error(f"ERROR: Invalid schema: {exc}")
            return False

    def push_data(self, data):
        if data_dict := self._check_valid(data):
            self.r.xadd(self.stream, {"value": json.dumps(data_dict, cls=NumpyArrayEncoder)})
            if data_dict.get("header"):
                if group_id := data_dict["header"].get("groupUUID"):
                    self.r.xadd(group_id, {"value": json.dumps(data_dict, cls=NumpyArrayEncoder)})
                    self.r.sadd(f'{str(self.stream)}-groups', str(group_id))
            return True
        return False

    def read_last(self):
        last_msgs = self.r.xrevrange(self.stream, count=1)
        if last_msgs:
            last_msgs = json.loads(last_msgs[0][1][b'value'].decode("utf-8").replace('\'', '\"'))
            return last_msgs
        else:
            return None

    def read_all(self):
        last_msgs = [json.loads(i[1][b'value'].decode("utf-8").replace('\'', '\"'))
                     for i in self.r.xrevrange(self.stream, count=10000)]
        if last_msgs:
            return last_msgs
        else:
            return None

    def get_msg_by_uuid(self, msg_uuid):
        last_msgs = [json.loads(i[1][b'value'].decode("utf-8").replace('\'', '\"'))
                     for i in self.r.xrevrange(self.stream, count=10000)]
        for i in last_msgs:
            if msg_uuid == i['header']['uuid']:
                return i
        return None

    def get_msg_by_block_id(self, msg_uuid):
        last_msgs = [json.loads(i[1][b'value'].decode("utf-8").replace('\'', '\"'))
                     for i in self.r.xrevrange(self.stream, count=10000)]
        for i in last_msgs:
            if msg_uuid == i['header']['block_id']:
                return i
        return None

    def get_group_imgs_by_block_id(self, msg_uuid):
        last_msgs = [json.loads(i[1][b'value'].decode("utf-8").replace('\'', '\"'))
                     for i in self.r.xrevrange(self.stream, count=10000)]
        x = []
        if last_msgs:
            for i in last_msgs:
                if msg_uuid == i['header'].get('block_id'):
                    x.append(i)
        return x[:3]

    def read_group(self, group_id):
        msgs = self.r.xrevrange(bytes(str(group_id).encode("utf-8")), count=1000)
        if msgs:
            return [json.loads(i[1][b'value'].decode("utf-8").replace('\'', '\"'))
                    for i in msgs]
        else:
            return None

    def delete_last_message(self):
        try:
            last_msg_id = self.r.xrevrange(self.stream, count=1)[0][0]
            self.r.xdel(self.stream, last_msg_id)
            return True
        except Exception as e:
            logging.error(f"delete_last_message: {e}")
            return False

    def delete_all_messages(self):
        try:
            self.r.xtrim(self.stream, maxlen=0)
            return True
        except Exception as e:
            logging.error(f"delete_all_messages: {e}")
            return False

    def delete_all_group_messages(self, group_id):
        try:
            self.r.xtrim(bytes(str(group_id).encode("utf-8")), maxlen=0)
            return True
        except Exception as e:
            logging.error(f"delete_all_group_messages: {e}")
            return False

    def get_groups_list(self):
        groups = self.r.smembers(f'{str(self.stream)}-groups')
        if groups:
            groups = [i.decode("utf-8") for i in groups]
        return groups or []


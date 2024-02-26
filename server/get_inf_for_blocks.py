from connector import *

my_block_id = '10.8.130.20'

try:
    r = RedisClient(host='192.168.0.101', port=6379, stream='data_for_itmo')
    print(r.get_msg_by_block_id(my_block_id))
except Exception as e:
    print(f"Ошибка при получении из Redis: {str(e)}")
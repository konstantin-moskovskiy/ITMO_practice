import time
from connector import *
import uuid
import click


def create_sheet_packet(block_ip):
    UUID = str(uuid.uuid4())
    header = {
        'version': '0.4',
        'uuid': UUID,
        'timestamp': int(time.time()),
        'packet': 'sheetInputCalculator',
        'consume_queue': 'calculator.input.sheet',
        'block_id': block_ip
    }

    sheet_data = {
        'innerSheetID': 'your_sheet_id',
        'cleaning': False,
        'reference': {
            'depth': 120.0,
            'length': 100.0,
            'width': 50.0
        }
    }

    packet = {
        'header': header,
        'body': {
            'sheet': [sheet_data]
        }
    }

    return packet

@click.command()
@click.option(
    "-i",
    "--block_ip",
    default=None
)
def main(block_ip):
    try:
        r = RedisClient(host='192.168.0.101', port=6379, stream='data_for_itmo')
        if block_ip != None:
            r.push_data(create_sheet_packet(block_ip))
            print(f"Пакет был отправлен на блок {block_ip}")
        else:
            ls = ['10.8.130.'+ str(i) for i in range(1, 23)]
            for ip in ls:
                r.push_data(create_sheet_packet(ip))
            print("Пакеты были отправлены на все блоки")
    except Exception as e:
        print(f'Ошибка при отправке в Redis: {str(e)}')

if __name__ == '__main__':
    main()
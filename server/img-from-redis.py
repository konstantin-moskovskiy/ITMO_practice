from connector import *
import click
import cv2
import numpy as np

@click.command()
@click.option(
    "-i",
    "--block_ip",
    default=None
)
def main(block_ip):
    try:
        r = RedisClient(host='192.168.0.101', port=6379, stream='data_from_itmo')
        if block_ip != None:
            ls = r.get_group_imgs_by_block_id(block_ip)
            img1 = np.array(ls[0]['body']['images'][0]["imgMapArray"], dtype=np.uint8)
            img2 = np.array(ls[1]['body']['images'][0]["imgMapArray"], dtype=np.uint8)
            img3 = np.array(ls[2]['body']['images'][0]["imgMapArray"], dtype=np.uint8)
            cv2.imshow('img1', img1)
            cv2.imshow('img2', img2)
            cv2.imshow('img3', img3)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Необходимо указать ip блока через ключ -i")
    except Exception as e:
        print(f'Ошибка при получении из Redis: {str(e)}')


if __name__ == '__main__':
    main()
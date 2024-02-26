from connector import *
import click

@click.command()
@click.option(
    "-i",
    "--block_ip",
    default=None
)
def main(block_ip):
    try:
        r = RedisClient(host='192.168.0.101', port=6379, stream='camera_status')
        if block_ip == None:
            ls = ['10.8.130.' + str(i) for i in range(1, 23)]
            for ip in ls:
                print(r.get_msg_by_block_id(ip))
        else:
            print(r.get_msg_by_block_id(block_ip))
    except Exception as e:
        print(f'Ошибка при получении из Redis: {str(e)}')


if __name__ == '__main__':
    main()
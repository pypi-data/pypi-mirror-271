from echo_logger import *


@monit_feishu()
def foo():
    raise IndexError('test')


if __name__ == '__main__':
    foo()

import socket
import threading

from tdxpy.base_socket_client import BaseSocketClient
from tdxpy.base_socket_client import CONNECT_TIMEOUT
from tdxpy.base_socket_client import TrafficStatSocket
from tdxpy.constants import SECURITY_EXCHANGE
from tdxpy.exceptions import TdxConnectionError
from tdxpy.heartbeat import HeartBeatThread
from tdxpy.reader import TdxDailyBarReader

from mootdx.logger import logger


class MooTdxDailyBarReader(TdxDailyBarReader):
    """感谢 bopomofo 的鼎力支持"""

    SECURITY_TYPE = [
        'SH_A_STOCK',
        'SH_B_STOCK',
        'SH_STAR_STOCK',
        'SH_INDEX',
        'SH_FUND',
        'SH_BOND',
        'SZ_A_STOCK',
        'SZ_B_STOCK',
        'SZ_INDEX',
        'SZ_FUND',
        'SZ_BOND',
    ]

    SECURITY_COEFFICIENT = {
        'SH_A_STOCK': [0.01, 0.01],
        'SH_B_STOCK': [0.001, 0.01],
        'SH_STAR_STOCK': [0.01, 0.01],
        'SH_INDEX': [0.01, 1.0],
        'SH_FUND': [0.001, 1.0],
        'SH_BOND': [0.001, 1.0],
        'SZ_A_STOCK': [0.01, 0.01],
        'SZ_B_STOCK': [0.01, 0.01],
        'SZ_INDEX': [0.01, 1.0],
        'SZ_FUND': [0.001, 0.01],
        'SZ_BOND': [0.001, 0.01],
    }

    def get_security_type(self, fname):

        exchange = str(fname[-12:-10]).lower()
        code_head = fname[-10:-8]

        if exchange == SECURITY_EXCHANGE[0]:
            if code_head in ['00', '30']:
                return 'SZ_A_STOCK'

            if code_head in ['20']:
                return 'SZ_B_STOCK'

            if code_head in ['39']:
                return 'SZ_INDEX'

            if code_head in ['15', '16', '18']:
                return 'SZ_FUND'

            if code_head in ['10', '11', '12', '13', '14']:
                return 'SZ_BOND'

            return 'SZ_OTHER'

        if exchange == SECURITY_EXCHANGE[1]:
            if code_head in ['60']:
                return 'SH_A_STOCK'

            if code_head in ['90']:
                return 'SH_B_STOCK'

            if code_head in ['68']:
                return 'SH_STAR_STOCK'

            if code_head in ['00', '88', '99']:
                return 'SH_INDEX'

            if code_head in ['50', '51', '58']:
                return 'SH_FUND'

            # if code_head in ['01', '10', '11', '12', '13', '14']:
            if code_head in ['01', '02', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']:
                return 'SH_BOND'

            return 'SH_OTHER'

        logger.error('Unknown security exchange !\n')
        raise NotImplementedError


class MooBaseSocketClient(BaseSocketClient):
    def __init__(self):
        super().__init__()
        self.client = None

    def connect(self, ip='101.227.73.20', port=7709, time_out=CONNECT_TIMEOUT, bindport=None, bindip='0.0.0.0'):
        """

        :param ip:  服务器ip 地址
        :param port:  服务器端口
        :param time_out: 连接超时时间
        :param bindport: 绑定的本地端口
        :param bindip: 绑定的本地ip
        :return: 是否连接成功 True/False
        """

        self.client = TrafficStatSocket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(time_out)

        logger.debug('connecting to server : %s on port :%d' % (ip, port))

        try:
            self.ip = ip
            self.port = port

            if bindport is not None:
                self.client.bind((bindip, bindport))

            self.client.connect((ip, port))
        except socket.timeout as e:
            logger.debug(e)
            logger.debug('connection expired')

            if self.raise_exception:
                raise TdxConnectionError('connection timeout error')

            return False
        except Exception as e:
            logger.debug(e)
            if self.raise_exception:
                raise TdxConnectionError('other errors')

            return False

        logger.debug('connected!')

        if self.need_setup:
            self.setup()

        if self.heartbeat:
            self.stop_event = threading.Event()
            self.heartbeat_thread = HeartBeatThread(self, self.stop_event, self.heartbeat_interval)
            self.heartbeat_thread.start()

        return self

    def disconnect(self):

        if self.heartbeat_thread and self.heartbeat_thread.is_alive():
            self.stop_event.set()

        if self.client:
            logger.debug('disconnecting')

            try:
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
                self.client = None
            except Exception as e:
                logger.debug(str(e))

                if self.raise_exception:
                    raise TdxConnectionError('disconnect err')

            logger.debug('disconnected')

    def setup(self):
        pass

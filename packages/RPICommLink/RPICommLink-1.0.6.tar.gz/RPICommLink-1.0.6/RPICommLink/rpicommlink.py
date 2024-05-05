import socket
import sys
import threading
import time


class RPICommLink:
    def __init__(self, rpi_port: int = 11451, password: str = '88888888'):
        """
        self.return_data:返回的数据，等待数据返回时为None。
        self.return_data:发送的数据，等待数据发送时为None。
        self.socket_list:当前连接的套接字列表。
        self.thread_now:当前正在运行的线程列表，用于存储正在等待接受数据的线程。
        self.data_event:线程间的事件通信。
        self.rpi_port:服务器打开的端口与客户端连接的端口，默认为11451。
        self.password:发送请求的密码。
        self.target_name:存储扫描到的设备名。
        self.connect_device:客户端已连接的设备。
        self.send_server_socket:发送的服务器套接字。
        """
        self.return_data = None
        self.socket_list = []
        self.threading_now = []
        self.data_event = threading.Event()
        self.data_event.clear()
        self.rpi_port = rpi_port
        self.password = password
        self.target_name = []
        self.connect_device = []
        self._send_server_socket = []

    def open(self, device_name: str = 'default', max_connect: int = 0, ip: str = None):
        """打开_server线程的函数

        它使用线程来启动服务器是为了实现非阻塞式的服务器启动。如果直接调用 _server 方法而不使用线程，
        那么在服务器启动过程中，主程序会被阻塞，直到服务器关闭或者达到最大连接数为止。

        通过在新的线程中启动服务器，主程序可以继续执行后续的操作，而不必等待服务器启动完成。
        当服务器启动后，它会在后台处理连接请求，而主程序可以继续执行其他任务，
        如处理用户输入、执行其他操作等。

        因此，使用线程来启动服务器可以提高程序的并发性和响应性，使程序更加灵活和高效。

        :param ip: ip地址，如果无法正确打开IP地址，请自行查看本地IP地址设置
        :param device_name:该设备名称，用于将设备名称发送给客户端
        :param max_connect:最大的客户端连接数量，如果它为0，则不作限制
        """
        listen_thread = threading.Thread(target=self._server, args=(device_name, max_connect, ip), daemon=True)
        listen_thread.start()

    def _server(self, device_name, max_connect, ip):
        """_server 的作用是启动一个服务器，用于监听客户端的连接请求，并根据一定条件接受或拒绝连接的线程。

        它负责创建一个 TCP 套接字，绑定到本机的 IP 地址和指定的端口号，然后在一个无限循环中等待客户端的连接请求。
        当有新的客户端连接时，检查连接数是否已达到最大限制 max_connect。达到最大限制发送给请求连接的客户端‘full’表示已达到最大限制，

        未达到最大限制 max_connect时，客户端有100ms的时间来请求加入服务器，请求通过后，将超时时间设置为无，
        并加入当前连接的套接字列表 self.socket_list，同时发送给客户端该设备名字 device_name
        """
        if ip is None:
            host_ip = get_host_ip()
        else:
            host_ip = ip

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host_address = (host_ip, self.rpi_port)
            server_socket.bind(host_address)
            server_socket.listen(5)
            print(f'\033[92m已在{host_ip}打开服务器\033[0m')
        except Exception:
            print('\033[93m无效IP地址\033[0m')
            return

        while True:
            client_socket, client_address = server_socket.accept()
            print(f'\033[92m{client_address}已连接成功\033[0m')
            if max_connect == 0 or len(self.socket_list) < max_connect:
                client_socket.settimeout(0.1)
                try:
                    password = client_socket.recv(1024)
                    client_socket.send(str(device_name).encode('utf-8'))
                    if password.decode('utf-8') == self.password:
                        time.sleep(0.1)
                        client_socket.send('ng3mxz7g'.encode('utf-8'))
                        client_socket.settimeout(None)
                        threading_socket = [client_socket, client_address]
                        self.socket_list.append(threading_socket)
                        recv_thread = threading.Thread(target=self._recv_threading,
                                                       args=(threading_socket,), daemon=True)
                        self.threading_now.append(threading_socket)
                        recv_thread.start()
                    else:
                        time.sleep(0.1)
                        client_socket.send('cjs8e77e'.encode('utf-8'))
                        print("\033[93m一台设备因为申请密码错误而被拒绝\033[0m")
                except socket.timeout:
                    print("\033[93m一台设备因为超时而被拒绝\033[0m")
            else:
                time.sleep(0.1)
                client_socket.send('ny6cz4ln'.encode('utf-8'))
                client_socket.close()
                print("\033[93m一台设备因为超过设定的最大限制而被拒绝\033[0m")

    def connect_list(self):  # 查询连接数量
        """在self.socket_list中获取套接字远程IP地址的函数

        :return: 返回一个当前连接的客户端IP列表
        """
        sock_list = []
        for info in self.socket_list:
            ip_address = info[0].getpeername()[0]
            sock_list.append(ip_address)
        return sock_list

    def wait(self):  # 等待连接，如果有连接返回True,阻塞线程
        """等待连接的函数

        使用无限循环来阻塞线程运行，通常和接收数据的recv_data函数组合使用

        :return: 当服务器有套接字连接时，返回True
        """
        while True:
            if len(self.socket_list) != 0:
                break
        return True

    def recv(self):
        """从已连接的多个套接字中异步接收数据的函数

        首先调用 wait_connect 方法，该方法会阻塞线程直到有连接建立。
        这是因为在没有连接的情况下，接收数据是没有意义的，所以该方法会一直等待直到至少有一个连接建立。

        一旦有连接建立，recv_data 方法会遍历当前连接的套接字列表 self.socket_list，
        为每个套接字创建一个接收数据的线程 recv_threading。如果某个套接字已经有对应的接收数据线程在运行，则不会重复创建。

        通过 self.data_event.wait() 来等待数据事件被设置。这意味着线程会一直阻塞，
        直到有数据被成功接收并存储在 self.return_data 中。

         一旦数据事件被设置，表示数据已经接收到，线程将继续执行。recv_data 方法将 self.return_data 中存储的数据返回给调用者，
         并将 self.return_data 设置为 None，以便下一次接收新的数据。

        :return:返回接收到的数据
        """
        if self.wait():
            for i in self.socket_list:
                if i not in self.threading_now:
                    recv_thread = threading.Thread(target=self._recv_threading, args=(i,), daemon=True)
                    self.threading_now.append(i)
                    recv_thread.start()
            if len(self.threading_now) == 0:
                try:
                    recv_thread = threading.Thread(target=self._recv_threading, args=(self.socket_list[0],),
                                                   daemon=True)
                    recv_thread.start()
                except Exception:
                    pass
            self.data_event.wait()  # 等待数据事件被设置
            return_data = self.return_data
            self.return_data = None
            self.data_event.clear()
            return return_data

    def _recv_threading(self, sock):
        """处理从客户端收到的数据的线程

        将当前处理的套接字 sock 添加到 self.threading_now 列表中，以便跟踪当前正在处理的线程。

        使用套接字对象的 recv 方法接收数据，如果没有接收到数据（recv_data 为空），说明连接已经关闭，
        所以关闭套接字，并从 self.socket_list 中移除该套接字。

        如果接收到了数据，将其解码为 UTF-8 格式，并存储在 self.return_data 属性中。
        通过 self.data_event.set() 设置数据事件，表示数据已经接收到。

        从 self.threading_now 列表中移除当前处理的套接字，表示该线程已完成。

        :param sock:需要接受到数据的套接字
        """
        try:
            recv_data = sock[0].recv(1024)
            if not recv_data:
                sock[0].close()
                self.socket_list.remove(sock)
                print(f"\033[93mError:一台设备断开了连接，当前设备数为{len(self.socket_list)}\033[0m")
            else:
                self.return_data = recv_data.decode('utf-8')
                self.data_event.set()  # 设置数据事件，表示数据已经接收到
            self.threading_now.remove(sock)
        except Exception:
            if sock in self.threading_now:
                self.threading_now.remove(sock)
            if sock in self.socket_list:
                self.socket_list.remove(sock)
            print(f"\033[91mError:一台设备连接异常中止 \033[0m")

    def _scan_port(self, ip, port, target):
        """扫描指定 IP 地址和端口，扫描局域网内的多个设备是否开放了指定的端口，并且尝试与这些设备建立连接。

        创建一个 TCP 套接字并设置超时时间为 1 秒。尝试连接指定的 IP 地址和端口。
        如果连接成功，发送密码给服务器端。
        接收服务器端返回的设备名字，并将其存储在 self.target_name 中。
        根据服务器端返回的状态进行相应的处理：
        如果状态是 'cjs8e77e'，表示密码错误，输出警告信息并关闭连接。
        如果状态是 'ng3mxz7g'，表示连接成功，将设备名字添加到 self.connect_device 列表中，并启动发送消息的线程。
        如果状态是 'ny6cz4ln'，表示服务器达到连接上限，输出错误信息。
        最后返回或者抛出异常。

        :param ip:要扫描的设备的IP地址。
        :param port:要扫描的端口号。
        :param target:目标设备的名称
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect((ip, port))
            if result is None:
                sock.send(self.password.encode('utf-8'))
                device_name = sock.recv(1024)
                self.target_name.append(device_name.decode('utf-8'))
                if device_name.decode('utf-8') == target:
                    sock.settimeout(None)
                    state = sock.recv(1024).decode('utf-8')
                    if state == 'cjs8e77e':
                        print(f'\033[93mWarning:由于申请密码不正确被拒绝 \033[0m')
                        self.target_name.pop()
                        self.target_name.append(f"{device_name.decode('utf-8')}(密码错误)")
                        sock.close()
                    elif state == 'ng3mxz7g':
                        self.connect_device.append(device_name.decode('utf-8'))
                        self._send_server_socket.append(sock)
                    elif state == 'ny6cz4ln':
                        print(f'\033[91mError:已达到服务器的设备连接上限 \033[0m')
            return
        except Exception:
            return None

    def connect(self, target_name: str = 'default', subnet_ip: str = None):
        """连接到服务器并尝试与指定设备建立连接的函数。

        如果无法构建局域网，请自行修改。

        获取本地主机的 IP 地址并构建局域网的子网。
        用线程遍历子网中的所有可能 IP 地址，并尝试连接到每个 IP 地址的指定端口。
        在连接成功时，发送密码给服务器端，并接收服务器返回的设备名称和状态。
        打印扫描到的设备名称。
        根据连接状态输出相应的信息。

        :param subnet_ip:子网，IP地址前三个数，格式为str’xxx.xxx.xx‘
        :param target_name: 指定的设备名字
        """
        if subnet_ip is None:
            local_ip = get_host_ip()  # 获取本地主机的IP地址
            subnet = '.'.join(local_ip.split('.')[:-1])  # 获取局域网子网
        else:
            subnet = subnet_ip
        port = self.rpi_port  # 要扫描的端口号
        threads = []
        for i in range(1, 255):
            ip = f"{subnet}.{i}"
            thread = threading.Thread(target=self._scan_port, args=(ip, port, target_name))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

        print(f'\033[92m找到了{self.target_name}\033[0m')
        if target_name in self.connect_device:
            print(f'\033[92m{target_name}连接成功\033[0m')
            check = []
            for item in self.target_name:
                if item in check:
                    print(f'\033[93m Warning：有多个同样的设备名密码正确，数据将同时发送，请确认！ \033[0m')
                    break
                check.append(item)
        else:
            if len(self.target_name) == 0:
                print(f'\033[91mError:无法找到任何设备 \033[0m')
            elif target_name not in self.connect_device:
                print(f'\033[93mError:没有找到{target_name}设备或密码不正确 \033[0m')

    def send(self, msg: str):
        """向服务器发送消息的函数

        :param msg:发送的信息
        """
        for sock in self._send_server_socket:
            try:
                sock.send(msg.encode('utf-8'))
            except Exception:
                print('\033[91mError:一个服务器发送失败！请确认是否有连接服务器 \033[0m')
                self._send_server_socket.remove(sock)
                if len(self._send_server_socket) == 0:
                    print('\033[91mError:无服务器连接 \033[0m')
                    sys.exit()


def get_host_ip():
    """
    查询本机IP地址
    :return:本机IP地址
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))
        ip = sock.getsockname()[0]
        sock.close()
        if ip is not None:
            return ip
    except Exception as e:
        ip = socket.gethostbyname(socket.gethostname())
        if ip != '127.0.0.1':
            return ip
        else:
            print(f'\033[93mWarning：无法通过互联网或自身获取IP，请自行设置IP \033[0m')
            sys.exit()


if __name__ == "__main__":
    pass

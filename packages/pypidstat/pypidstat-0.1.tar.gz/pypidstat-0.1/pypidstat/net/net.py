import os
import re
import pcap
import dpkt
import threading
import time
import copy


class Net:

    # params:
    #    dev: the interface to be monitored, such as eth0
    #    interval: the interval in seconds that refresh the map ( tcp connection=> pid )
    def __init__(self, dev, interval):
        self.__dev = dev
        self.__interval = interval
        self.__pcap = pcap.pcap(dev)
        self.__refresh_map()
        self.__proc_traffic = {}
        self.__thread_map = threading.Thread(target=self.__thread_map_func)
        self.__thread_map.setDaemon(True)
        self.__thread_map.start()
        self.__thread_cap = threading.Thread(target=self.__thread_cap_func)
        self.__thread_cap.setDaemon(True)
        self.__thread_cap.start()
        self.__fd = open('/proc/net/dev')

    def __del__(self):
        # 暂时没有发现强制结束线程的办法
        # self.__thread_map.stop()
        # self.__thread_cap.stop()
        self.__fd.close()

    def __refresh_map(self):
        map_inode_pid = {}
        regex = re.compile('^\\d+$')
        dirs = os.listdir('/proc')
        for d in dirs:
            if regex.match(d):
                pid = int(d)
                try:
                    fds = os.listdir('/proc/%s/fd' % d)
                except:
                    continue
                for f in fds:
                    try:
                        link = os.readlink('/proc/%s/fd/%s' % (d, f))
                    except:
                        continue
                    if link.startswith('socket:'):
                        inode = int(link[8:-1])
                        map_inode_pid[inode] = pid
        map_addr_inode = {}
        fd = open('/proc/net/tcp')
        lines = fd.readlines()
        fd.close()
        for line in lines[1:]:
            items = line.split()
            local = self.__to_normal_addr_format(items[1])
            remote = self.__to_normal_addr_format(items[2])
            address = '%s-%s' % (local, remote)
            inode = int(items[9])
            map_addr_inode[address] = inode
        map_addr_pid = {}
        for addr, inode in map_addr_inode.items():
            try:
                pid = map_inode_pid[inode]
            except:
                continue
            map_addr_pid[addr] = pid
        self.__map_addr_pid = map_addr_pid

    def __to_normal_addr_format(self, addr):
        ip, port = addr.split(':', 2)
        ip = '.'.join([str(int(ip[i:i + 2], 16)) for i in range(0, len(ip), 2)][::-1])
        port = int(port, 16)
        return '%s:%d' % (ip, port)

    def __thread_map_func(self):
        while True:
            self.__refresh_map()
            time.sleep(self.__interval)

    def __thread_cap_func(self):
        for cap_time, cap_raw in self.__pcap:
            frame = dpkt.ethernet.Ethernet(cap_raw)
            if isinstance(frame.data, dpkt.ip.IP):
                packet = frame.data
                src_ip = '.'.join([str(ord(d)) for d in list(packet.src)])
                dst_ip = '.'.join([str(ord(d)) for d in list(packet.dst)])
                if isinstance(packet.data, dpkt.tcp.TCP):
                    datagram = packet.data
                    src_port = datagram.sport
                    dst_port = datagram.dport
                    src = '%s:%d' % (src_ip, src_port)
                    dst = '%s:%d' % (dst_ip, dst_port)
                    try:
                        pid = self.__map_addr_pid['%s-%s' % (src, dst)]
                        direction = 'send'
                    except:
                        try:
                            pid = self.__map_addr_pid['%s-%s' % (dst, src)]
                            direction = 'recv'
                        except:
                            continue
                    if not self.__proc_traffic.has_key(pid):
                        traffic = [0, 0, 0, 0]
                        self.__proc_traffic[pid] = traffic
                    else:
                        traffic = self.__proc_traffic[pid]
                    if direction == 'send':
                        traffic[0] += 1
                        traffic[1] += len(datagram.data)
                    else:
                        traffic[2] += 1
                        traffic[3] += len(datagram.data)

    # network traffic of the network interface
    #   return (send packets, send bytes, recv packets, recv bytes)
    def traffic(self):
        self.__fd.seek(0)
        lines = self.__fd.readlines()
        for line in lines:
            items = line.split()
            if items[0][:-1] == self.__dev:
                recv_bytes = int(items[1])
                recv_packets = int(items[2])
                send_bytes = int(items[9])
                send_packets = int(items[10])
                return send_packets, send_bytes, recv_packets, recv_bytes

    # network traffic of given process,
    #    return (send packets, send bytes, recv packets, recv bytes)
    def proc_traffic(self, pid):
        return self.__proc_traffic[pid] if self.__proc_traffic.has_key(pid) else 0, 0, 0, 0)

    # network traffic of all processes that have sent or received packets
    #    return dict { pid = > (send packets, send bytes, recv packets, recv bytes) }
    def proc_traffic_all(self):
        return copy.deepcopy(self.__proc_traffic)

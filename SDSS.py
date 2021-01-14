""" /////////////////////////////////////////////////////////
                Simple Delay Sync Service (SDSS)
    ///////////////////////////////////////////////////////// """

""" Coode skeleton was provided by Computer Networks Course Teaching Assistants """
""" This project is a mini introduction to peer-to-peer networking. """

######################################
####            Imports            ###
######################################
import sys
import os
import threading
import socket
import datetime
from datetime import timezone
import time
import uuid
import struct


# https://bluesock.org/~willkg/dev/ansi.html
ANSI_RESET = "\u001B[0m"
ANSI_RED = "\u001B[31m"
ANSI_GREEN = "\u001B[32m"
ANSI_YELLOW = "\u001B[33m"
ANSI_BLUE = "\u001B[34m"

_NODE_UUID = str(uuid.uuid4())[:8]


def print_yellow(msg):
    print(f"{ANSI_YELLOW}{msg}{ANSI_RESET}")


def print_blue(msg):
    print(f"{ANSI_BLUE}{msg}{ANSI_RESET}")


def print_red(msg):
    print(f"{ANSI_RED}{msg}{ANSI_RESET}")


def print_green(msg):
    print(f"{ANSI_GREEN}{msg}{ANSI_RESET}")


def get_broadcast_port():
    return 35498


def get_node_uuid():
    return _NODE_UUID


class NeighborInfo(object):
    def __init__(self, delay, last_timestamp, broadcast_count, ip=None, tcp_port=None):
        # Ip and port are optional, if you want to store them.
        self.delay = delay
        self.last_timestamp = last_timestamp
        self.broadcast_count = broadcast_count
        self.ip = ip
        self.tcp_port = tcp_port


############################################
#######  Y  O  U  R     C  O  D  E  ########
############################################
""" /////////////////////
       Global Variables
    ///////////////////// """
port = 0
NewPort = 0
node_uuid = 0

# Don't change any variable's name.
# Use this hashmap to store the information of your neighbor nodes.
neighbor_information = {}
# Leave the server socket as global variable.

# Server TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1',0)) 
server.listen()

# Broadcaster UDP
broadcaster= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcaster.settimeout(4)


# Send the broadcast Message Function
def send_broadcast_thread(port_number):
    global broadcaster
    global node_uuid
    node_uuid = get_node_uuid()
    
    while True:
        Message  = str(node_uuid) + " ON " + str(port_number)
        Message_V2 = Message.encode("utf-8")
        broadcaster.sendto(Message_V2, ('255.255.255.255', get_broadcast_port()))
        print_yellow("Broadcast Message is sent")
        time.sleep(1)   # Leave as is.
    pass


# Chef If Node Recieve Itself Function
def checkIfsameNode (message):
    global node_uuid 
    global neighbor_information
    if (node_uuid != message[0] and neighbor_information.get(message[0]) == None):
        #print_green("Added Successfully") 
        return 1
    elif (node_uuid != message[0] and neighbor_information.get(message[0]) != None):
        return 2
    else: 
        #print_red("Ignored")  
        return 0


# Receive the broadcast Message Function
def receive_broadcast_thread():
    """
    Receive broadcasts from other nodes,
    launches a thread to connect to new nodes
    and exchange timestamps.
    """
    global neighbor_information
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.bind(('', get_broadcast_port()))

    while True:
        data, (ip, port) = client.recvfrom(4096)
        data_v2 = data.decode("utf-8")
        parsed = data_v2.split(" ")
        print(parsed)
        newnodeflag=checkIfsameNode(parsed)

        if(newnodeflag == 1):
            tcpClient=daemon_thread_builder(exchange_timestamps_thread,args=(parsed[0],"127.0.0.1",parsed[2],))
            tcpClient.start()  
            tcpClient.join()
        elif(newnodeflag == 2):
            x = neighbor_information.get(parsed[0])
            neighbor_information.update({parsed[0]:NeighborInfo(x.delay,x.last_timestamp,x.broadcast_count+1)})
            if (x.broadcast_count == 9):  
                neighbor_information.pop(parsed[0])

        print_blue(f"RECV: {data} FROM: {ip}:{port}")
        
        
# TCP Server Thread Function 
def tcp_server_thread(id, tcpPort):
    """
    Accept connections from other nodes and send them
    this node's timestamp once they connect.
    """
    global server
    
    # TCP Connection
    conn,adrr = server.accept()
    received_time_stamp = struct.unpack('!f', conn.recv(4096))[0]
    
    exchange = daemon_thread_builder(CalcDelay, args=(received_time_stamp, id,tcpPort ))
    exchange.start()
    exchange.join()

    pass


# Exchange Timestamp Between Two Nodes Function
def exchange_timestamps_thread(other_uuid: str, other_ip: str, other_tcp_port: int):
    """
    Open a connection to the other_ip, other_tcp_port
    and do the steps to exchange timestamps.

    Then update the neighbor_info map using other node's UUID.
    """
    tcpserver=daemon_thread_builder(tcp_server_thread, args=(other_uuid, other_tcp_port))

    SENDER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SENDER.connect((other_ip,int(other_tcp_port)))
    address = (other_ip, int(other_tcp_port))
    time_now = datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()
    SENDER.sendto(struct.pack('!f', time_now), address)
    
    tcpserver.start()
    tcpserver.join()
    SENDER.close()

    pass


# Calculate Delay Function
def CalcDelay(sentTime, id, tcpPort):
    if(sentTime != ""): # Only calculate delay when there is a value received for timestamp
        Now = datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()
        Delay = abs(Now - sentTime)
        print_red(f"Delay From Device => [ {id} ] is => {str(Delay)}ms")
        x = NeighborInfo(Delay,Now,1)
        neighbor_information.update({id: x}) # Add New Neighbor
    pass
    

# Create Threads Function
def daemon_thread_builder(target, args=()) -> threading.Thread:
    """
    Use this function to make threads. Leave as is.
    """
    th = threading.Thread(target=target, args=args)
    th.setDaemon(True)
    return th


# Start Sending and Receiving Broadcast Message
def entrypoint():
   # Send Broadcast
    global server
    port=server.getsockname()[1]
    
    # Receive Broadcast
    receiver=daemon_thread_builder(receive_broadcast_thread)
    sender=daemon_thread_builder(send_broadcast_thread,args=(port,))
    
    sender.start()
    receiver.start()

    sender.join()
    receiver.join()

    pass

    
############################################
############################################


def main():
    """
    Leave as is.
    """
    print("*" * 50)
    print_red("To terminate this program use: CTRL+C")
    print_red("If the program blocks/throws, you have to terminate it manually.")
    print_green(f"NODE UUID: {get_node_uuid()}")
    print("*" * 50)
    time.sleep(2)   # Wait a little bit.
    entrypoint()


if __name__ == "__main__":
    main()

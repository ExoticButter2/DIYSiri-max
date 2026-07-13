import socket

def ReceiveStrict(byteAmount, connection:socket.socket):
    dataBuffer = bytearray()
    
    while byteAmount > 0:
        try:
            chunk = connection.recv(byteAmount)
            
            if not chunk:
                print("Socket closed")
                break
            
            byteAmount -= len(chunk)
            dataBuffer.extend(chunk)
        except connection.timeout:
            connection.close()
            connection.connect(("192.168.178.162", 4000))

    return dataBuffer
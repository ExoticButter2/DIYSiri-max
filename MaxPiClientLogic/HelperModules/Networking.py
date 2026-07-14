import socket

def ReceiveStrict(byteAmount, connection:socket.socket):
    dataBuffer = bytearray()
    
    while byteAmount > 0:
        chunk = connection.recv(byteAmount)
        
        if not chunk:
            print("Socket closed")
            break
        
        byteAmount -= len(chunk)
        dataBuffer.extend(chunk)

    return dataBuffer
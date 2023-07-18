import socket
my_socket = socket.socket()
my_socket.connect(("10.0.0.14", 8820))
my_socket.send("Omer".encode())
data = my_socket.recv(1024).decode()
print("The server sent " + data)
my_socket.close()
import socket
import pygame

size = (100, 100)
SCREEN = pygame.display.set_mode(size)


def main():
    pygame.init()

    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8820))
    server_socket.listen()
    print('server is up and running')
    (client_socket, client_address) = server_socket.accept()
    print('client connected')
    pressed = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    client_socket.send('SPACE'. encode())
                elif event.key == pygame.K_LEFT:
                    client_socket.send('LEFT'.encode())
                elif event.key == pygame.K_RIGHT:
                    client_socket.send('RIGHT'.encode())
                elif event.key == pygame.K_UP:
                    client_socket.send('UP'.encode())
                elif event.key == pygame.K_DOWN:
                    client_socket.send('DOWN'.encode())


    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
    
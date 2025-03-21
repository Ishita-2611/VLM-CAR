import socket
from car_controller import CarController

car = CarController()

HOST = "0.0.0.0"
PORT = 5001

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Listening on {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if not data:
                    continue
                
                command = data.decode().strip()
                print(f"Received Command: {command}")
                
                car.execute(command)

if __name__ == "__main__":
    start_server()

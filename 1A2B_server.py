import socket
import random 

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 7000 #Port範圍介於1024~65535，其中0~1023為系統保留不可使用
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

#Function to Get The Correct Answer
def get_ans():
    seed = []
    for i in range(0,9): seed.append(i+1)

    Ans = ""
    for i in random.sample(seed ,4):
        Ans += str(i)
    return Ans



def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connect = True
    while connect:
        #Send Correct Answer to Client
        sendanstoclient = get_ans()
        conn.send(sendanstoclient.encode(FORMAT))

        guess = conn.recv(1024).decode(FORMAT)
        print('Receive player\s name', guess)
        totalrounds = conn.recv(1024).decode(FORMAT)
        print('Player', guess , 'guessed',totalrounds,'finally find the correct answer!')
        sendtoclient = input('If Server wants to quit enter quit: ')
        if sendtoclient == 'quit':
            connect = False
        else:
            conn.send(sendtoclient.encode(FORMAT))
            print(totalrounds)

    conn.close()
    s.close()


def start():
    s.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    conn, addr = s.accept()
    handle_client(conn, addr)


print("[STARTING] Server is starting...")
print ("Game start!!")
start()


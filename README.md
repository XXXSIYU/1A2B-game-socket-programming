# Socket Programming Project
## 1A2B Simple Game
#### 猜數字遊戲 1A2B，製作一個簡單的小遊戲，猜出四位數字。當位置且數字正確時玩家端會顯示 A，當數字正確但擺放位置錯誤時，玩家端會顯示 B。
#### 正確答案於Server 端產生並透過 socket 連接將答案傳送至 client 也就是玩家端，再做後續的判斷。
## Server 
### 求出正確答案的 get_ans() function
```
import random
...
#Function to Get The Correct Answer
def get_ans():
    seed = []
    for i in range(0,9): seed.append(i+1)

    Ans = ""
    for i in random.sample(seed ,4):
        Ans += str(i)
    return Ans
```
### Server handle to client
1. #### Send correct answer to client/player
```
#Send Correct Answer to Client
sendanstoclient = get_ans()
conn.send(sendanstoclient.encode(FORMAT))
```
2. #### When player enter their names, server will receive.
```
#Recieve Player's Name From Client
playername = conn.recv(1024).decode(FORMAT)
print("Receive player's name", playername)
```
3. #### Player win the game, server will print player's name and their total guess sent by client.
```
#When Player Win Recieve Total Guess Counts From Server
totalrounds = conn.recv(1024).decode(FORMAT)
print('Player', playername , 'guessed',totalrounds,'finally find the correct answer!')
```
### handle_client() function
```
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connect = True
    while connect:
        #Send Correct Answer to Client
        sendanstoclient = get_ans()
        conn.send(sendanstoclient.encode(FORMAT))

        #Recieve Player's Name From Client
        playername = conn.recv(1024).decode(FORMAT)
        print("Receive player's name", playername)

        #When Player Win Recieve Total Guess Counts From Server
        totalrounds = conn.recv(1024).decode(FORMAT)
        print('Player', playername , 'guessed',totalrounds,'finally find the correct answer!')
        sendtoclient = input('If Server wants to quit enter quit: ')
        if sendtoclient == 'quit':
            connect = False
        else:
            conn.send(sendtoclient.encode(FORMAT))
            print(totalrounds)
            start()

    conn.close()
    s.close()
```
## Client
### correct_ans()
### 判斷幾A幾B的function，也就是說將Server端求出的正確答案與Player所猜數字進行比較。
#### 數字不可以重複，且一定要為四位才可判斷。
```
def correct_ans(Ans,guess):
    count = 1
    #print ("Ans : %s" %Ans) # debug
    while Ans!= guess:
        print ("============================")    
        print ('ROUND : %s' %count)
        guess = input("Your answer is : ")
        if len(guess) != 4:
            print ("Enter 4 numbers.")
            continue
        elif len(set(guess)) != 4:
            print ("Enter 4 different numbers.")
            continue
        count +=1
        a = 0
        b = 0
        for i in range(4):
            if guess[i]== Ans[i]:
                a+=1
            elif guess[i] in Ans:
                b+=1
        print ("This round you got %sA %sB." %(a,b))

    print ("You Win!")
    return count
```
### Send() function
### 將Player名字傳送到Server端，並再猜到正確數字時回傳總共猜了幾次。
```
def send():
    while True:
        guesstoserver = input('Please enter your name：')
        if guesstoserver == 'quit':
            c.close() 
            sys.exit(0)
        else:
            c.send(guesstoserver.encode(FORMAT)) 
            #print('Recieve：',c.recv(1024).decode(FORMAT)) 


        ans = c.recv(1024).decode(FORMAT)
        totalcount = str(correct_ans(ans, guesstoserver))
        c.send(totalcount.encode(FORMAT))
        c.close
        sys.exit(0)
```
## 執行步驟
1. 在終端機中開啟server檔

![](https://i.imgur.com/aXhe6ZD.png)

2. 到程式碼所在的資料夾，右鍵，開啟client檔

![](https://i.imgur.com/S05pT5v.png)

---

##### 以下為Client 也就是Player畫面
3. 連接成功client畫面

![](https://i.imgur.com/A7gdn4Z.png)

4. Player輸入名稱即可開始猜題

![](https://i.imgur.com/R5r6pLt.png)

---

##### Server端
5. Server 端在Player輸入名稱後，會收到並顯示在畫面上

![](https://i.imgur.com/pyXebIE.png)

---

##### 回到Player畫面
6. 開始玩遊戲，可以看到每猜完一次按下Enter後會顯示提示第幾輪猜題

![](https://i.imgur.com/yDdxmpX.png)

7. 直到猜到正確答案為止，結束Client程式

![](https://i.imgur.com/24qpFUv.png)

---

##### Server端
8. Server端可以看到Player名稱以及猜了幾次得到正確答案

![](https://i.imgur.com/JrAJKm0.png)

9. 關閉Server需輸入"quit"

![](https://i.imgur.com/bLvYI3T.png)

---

##### Player輸入不符合規定時的畫面
![](https://i.imgur.com/ftrq8Gh.png)



---

## Server.py
```
import socket
import random 

SERVER = socket.gethostbyname(socket.gethostname())
PORT = #Port範圍介於1024~65535，其中0~1023為系統保留不可使用
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

        #Recieve Player's Name From Client
        playername = conn.recv(1024).decode(FORMAT)
        print("Receive player's name", playername)

        #When Player Win Recieve Total Guess Counts From Server
        totalrounds = conn.recv(1024).decode(FORMAT)
        print('Player', playername , 'guessed',totalrounds,'finally find the correct answer!')
        sendtoclient = input('If Server wants to quit enter quit: ')
        if sendtoclient == 'quit':
            connect = False
        else:
            conn.send(sendtoclient.encode(FORMAT))
            print(totalrounds)
            start()

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


```
## Client.py
```
import socket
import sys

PORT =  #write yours
FORMAT = 'utf-8'
SERVER = #Server IP
ADDR = (SERVER, PORT)

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(ADDR) 

def correct_ans(Ans,guess):
    count = 1
    #print ("Ans : %s" %Ans) # debug
    while Ans!= guess:
        print ("============================")    
        print ('ROUND : %s' %count)
        guess = input("Your answer is : ")
        if len(guess) != 4:
            print ("Enter 4 numbers.")
            continue
        elif len(set(guess)) != 4:
            print ("Enter 4 different numbers.")
            continue
        count +=1
        a = 0
        b = 0
        for i in range(4):
            if guess[i]== Ans[i]:
                a+=1
            elif guess[i] in Ans:
                b+=1
        print ("This round you got %sA %sB." %(a,b))

    print ("You Win!")
    return count


def send():
    while True:
        nametoserver = input('Please enter your name：')
        if nametoserver == 'quit':
            c.close() 
            sys.exit(0)
        else:
            c.send(nametoserver.encode(FORMAT)) 
            #print('Recieve：',c.recv(1024).decode(FORMAT)) 


        ans = c.recv(1024).decode(FORMAT)
        totalcount = str(correct_ans(ans, nametoserver))
        c.send(totalcount.encode(FORMAT))
        c.close
        sys.exit(0)
            


print("Client connect to server")

print ("Game start!!")
print ("Please enter 4 numbers and press \"enter\"")
send()
```
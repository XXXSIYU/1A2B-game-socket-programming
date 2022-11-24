import socket
import sys

PORT = 7000
FORMAT = 'utf-8'
SERVER = "192.168.56.1" #Server IP
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
            


print("Client connect to server")

print ("Game start!!")
print ("Please enter 4 numbers and press \"enter\"")
send()
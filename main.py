import socket
import time
import os
import sys

class bot:
    def __init__(self):
        self.server = "irc.chat.twitch.tv"
        self.port = 6667
        self.channel = "#treeedbot"
        self.bot_username = "Bot"
        self.operators = ["treeed", "same1lo"]
        self.waitTime = 0.5
        
        

    def connect(self):
        self.irc = socket.socket()
        self.irc.connect((self.server, self.port))

        #c0uvj4e8hb1kpn6nm2bqu77ahp08qv

        self.irc.send(f"PASS oauth:il2vyzcmw1ge3ktaeoc7cd5uwm7zwa\r\n".encode("utf-8"))
        self.irc.send(f"NICK {self.bot_username}\r\n".encode("utf-8"))
        self.irc.send(f"JOIN {self.channel}\r\n".encode("utf-8"))     

        self.sendMSG(self.channel, "Bot started!")
        
        while True:
            data = self.irc.recv(4096).decode("utf-8")
            
            user_index_start = data.find(":") + 1
            user_index_end = data.find("!")
            self.username = data[user_index_start:user_index_end]

            
            print(data)
            if data:
                if "PING" in data:
                    self.irc.send(f"PONG :{data}\r\n".encode("utf-8"))
                
                self.checkCommand(data)

    def help_command(self, username):
        msg = f"@{username} https://app.gitbook.com/o/pQ6VBNqYBzgA89foKuEr/s/evPrE4CfiskJGS9c4Y70/"
        self.sendMSG(self.channel, msg)
    
    def reload_command(self):
        self.sendMSG(self.channel, "reloading...")

        print("argv was",sys.argv)
        print("sys.executable was", sys.executable)
        print("restart now")

        os.execv(sys.executable, ['python'] + sys.argv)
    
    def checkCommand(self, data):
        parts = data.split()
        username = parts[0][1:].split('!')[0]

        try:
            if username in self.operators:
                if ">" in data:
                    time.sleep(self.waitTime)
                                
                    if ">echo" in data:
                        echo_index = parts.index(':>echo')

                        echo_content = ' '.join(parts[echo_index + 1:])

                        print(f"Username: {username}")
                        print(f"Echo Content: {echo_content}")
                        
                        self.sendMSG(self.channel, f"{username} > {echo_content}")
                                        
                    elif ">exit" in data:
                        self.sendMSG(self.channel, "The bot is quitting....")
            
                        time.sleep(self.waitTime)

                        self.irc.send("QUIT\r\n".encode("utf-8"))
                        self.irc.close()
                        exit()
                        
                    elif ">spam" in data:
                        spam_index = parts.index(':>spam')
                        
                        for x in range(int(parts[spam_index + 1:][0])):
                            self.sendMSG(self.channel, f"{' '.join(parts[spam_index + 2:])}")
                                        
                    elif ">return" in data:
                        return_index = parts.index(':>return')

                        return_content = ' '.join(parts[return_index + 1:])

                        self.sendMSG(self.channel, f"{username} > {eval(return_content)}")
                        
                    elif ">reload" in data:
                        self.reload_command()

                    elif ">op" in data:
                        self.sendMSG(self.channel, "op")

                    elif ">help" in data:
                        self.help_command(self.username)

                    elif ">sendto" in data:
                        sendto_index = parts.index(':>sendto')

                        sendto_content = ' '.join(parts[sendto_index + 2:])

                        self.sendMSG(f"#{parts[sendto_index + 1:][0]}", sendto_content)

                    elif ">todo" in data:
                        self.sendMSG(self.channel, "todo")

                    elif ">switch" in data:
                        self.sendMSG(self.channel, "switch")
                    
        except Exception as e:
            self.sendMSG(self.channel, f"{e}! Bdw der Error ist von Python deswegen so schlecht LuL")
                

    def sendMSG(self, channel, message):
        self.irc.send(f"PRIVMSG {channel} :{message}\r\n".encode("utf-8"))

    
    def run(self):
        print(123)
        self.connect()

if __name__ == "__main__":
    Bot = bot()
    Bot.run()
import socket
import configparser
import os
import time

import customtkinter
import sys


config = configparser.ConfigParser()
if os.path.isfile("config.ini"):
    config.read('config.ini')
else:
    config.add_section('User')
    config.set('User', 'username', 'user')
    config.add_section('Network')
    config.set('Network', 'port', '11719')
    with open('config.ini', 'w', encoding="utf-8") as config_file:
        config.write(config_file)
    config.read('config.ini')

nickname = config.get('User', 'username')
port = config.get('Network', 'port')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('0.0.0.0', int(port)))

list_users = ["sergey", "artem", "sofia", "mark", "artem", "sofia"]


def enter(event):
    o_message = nickname + ": " + sender.get() + "\n"
    if len(o_message) != 0:
        sender.delete(0, "end")
        print("message " + o_message)
        # chat.insert("end", o_message)
        s.sendto(o_message.encode(), ('255.255.255.255', int(port)))


def priem():
    global list_users
    chat.see("end")
    s.setblocking(False)
    try:
        i_message = s.recv(128).decode()
        if "#" in i_message:

            print("user", i_message[1:])
            if i_message[1:] in list_users:
                print(list_users)
            else:
                list_users.append(i_message[1:])


        elif "*" in i_message:
            list_users.remove(i_message[1:])


        elif "@" in i_message and nickname in i_message:
            chat.insert("end", "\n\n####################\n" + i_message + "####################\n\n")

        elif "@" in i_message:
            pass
        else:
            chat.insert("end", i_message)

    except:
        app.after(10, priem)

        return

    app.after(10, priem)

    # return


def on_closing():
    s.sendto(f"{nickname} ушел из сети\n".encode(), ('255.255.255.255', int(port)))
    s.sendto(f"*{nickname}".encode(), ('255.255.255.255', int(port)))
    app.destroy()


def opening():
    s.sendto(f"{nickname} в сети\n".encode(), ('255.255.255.255', int(port)))


def writing(event):
    if "@" in sender.get():
        pass
    else:
        s.sendto(f"{nickname} печатает...\n".encode(), ('255.255.255.255', int(port)))


def private(l):
    print(l)
    sender.delete(0, "end")
    sender.insert(0, "@" + list_users[l] + ": ")


def list_upd():
    nick = "#" + nickname
    s.sendto(nick.encode(), ('255.255.255.255', int(port)))

    i = 1
    for ul in list_users:
        # print(ul)
        user = customtkinter.CTkButton(app, text=ul, fg_color="#212F3D", hover_color="#2C3E50", text_color="#BABABA",
                                       font=("tahoma", 12, "bold"), command=lambda l=i: private(l - 1))
        user.grid(row=i, column=1, padx=2, pady=2, sticky="n")
        # user.bind("<Button-1>", lambda l = i: private(l))
        i += 1

    app.after(1000, list_upd)


def save(self):
    config.set('User', 'username', prof1.get())
    with open('config.ini', 'w', encoding="utf-8") as config_file:
        config.write(config_file)
    os.execv(sys.executable, ["python"] + sys.argv)

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)


app = customtkinter.CTk()
app.title('Local_chat 1.0 [stable]')
app.resizable(False, False)
app.geometry('+800+400')
app.iconbitmap("./icon.ico")
app.configure(fg_color="#17202A")
app.grid_columnconfigure(0, weight=1)
# app.rowconfigure(0, weight=1)
# customtkinter.set_default_color_theme("green")



prof = customtkinter.CTkLabel(app, text="Мой ник-нейм:", fg_color="#2C3E50", text_color="#BABABA", font=("tahoma", 12, "bold"))
prof.grid(row=0, column=0, padx=4, pady=4, sticky="nwe")

prof1 = customtkinter.CTkEntry(app, fg_color="#2C3E50", text_color="#BABABA", font=("tahoma", 12, "bold"), border_color="#2C3E50")
prof1.grid(row=0, column=1, padx=4, pady=4, sticky="nwe")
prof1.insert(0, nickname)
prof1.bind('<Return>', save)

# поле чата
chat = customtkinter.CTkTextbox(app, fg_color="#1C2833", text_color="#BABABA", font=("tahoma", 12, "bold"))
chat.grid(row=1, column=0, padx=4, pady=2, sticky="ewns", rowspan=20)

# поле ввода
sender = customtkinter.CTkEntry(app, fg_color="#2C3E50", text_color="#BABABA", font=("tahoma", 12, "bold"),
                                border_color="#2C3E50")
sender.grid(row=21, column=0, padx=4, pady=4, columnspan=2, sticky="ews") #, columnspan=2
sender.bind('<Return>', enter)
sender.bind("<FocusIn>", writing)

# надпись
footer = "©Local_chat 1.0 [stable]  Разработчик: Руслан Юрьевич К., 2023. \nРаспространяется под лицензией GPL v3. Все права защищены."
l = customtkinter.CTkLabel(app, text=footer, text_color="#BABABA")
l.grid(row=22, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

app.after(10, priem)
app.after(10, list_upd())
app.protocol("WM_DELETE_WINDOW", on_closing)
app.after_idle(opening)
app.mainloop()

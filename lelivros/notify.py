from email.mime.text import MIMEText
import smtplib

class EmailNotification():
    books = list()
    addresses = list()
    body_model = '<a href="{url}">{desc}</a>\n'

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def add_book(self, book):
        self.books.append(book)

    def add_address(self, address):
        self.addresses.append(address)

    def send(self):
        body = str()
        for desc, url in self.books:
            body += self.body_model.format(desc=desc, url=url)

        msg = MIMEText(body, 'html')
        msg['From'] = self.email
        msg['To'] = ', '.join(self.addresses)
        msg['Subject'] = "LeLivros - Novidades"

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email, self.password)
        text = msg.as_string()
        server.sendmail(self.email, self.addresses, text)
        server.quit()

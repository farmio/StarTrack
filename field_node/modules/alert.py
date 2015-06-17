#adn
import requests
import adnpy
#email
import smtplib
import email.utils
from email.MIMEText import MIMEText


class Adn:
    def __init__(self, credentials):
        self.access_token = credentials['access_token']
        self.default_recipient = credentials['recipient']
        adnpy.api.add_authorization_token(self.access_token)

    def pm(self, text, recipient=None):
        if not(recipient): recipient = self.default_recipient
        try:
            msg, meta = adnpy.api.create_message( 'pm', data={'text': text,
                'destinations': [recipient]} )
            return meta['code']
        except requests.exceptions.ConnectionError:
            print('damn no internet')
            return 599                  #maybe a string?


class Email:
    def __init__(self, credentials):
        self.server = smtplib.SMTP(credentials['smtp_server'],
                                   credentials['smtp_port'])
        self.author = credentials['from_name']
        self.from_email = credentials['from_email']
        self.default_recipient = credentials['recipient']
        self.username = credentials['login']
        self.password = credentials['password']

    def send_mail(self, text, recipient=None, subject='StarTrack Notofication'):
        if not(recipient): recipient = self.default_recipient
        msg = MIMEText(text)
        msg.set_unixfrom(self.author)
        msg['To'] = recipient
        msg['From'] = email.utils.formataddr((self.author, self.from_email))
        msg['Subject'] = subject

        server = self.server
        try:
            server.set_debuglevel(True)

            # identify ourselves, prompting server for supported features
            server.ehlo()

            # If we can encrypt this session, do it
            if server.has_extn('STARTTLS'):
                server.starttls()
                server.ehlo() # re-identify ourselves over TLS connection

            server.login(self.username, self.password)
            server.sendmail(self.from_email, [recipient], msg.as_string())
        finally:
            server.quit()


class Alert:
    @staticmethod
    def spy(status):
        pass

    @staticmethod
    def now(message, destination=None):
        pass

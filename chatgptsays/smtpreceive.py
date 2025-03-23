import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP as SMTPBase, Envelope

class CustomSMTPHandler(SMTPBase):
    async def handle_HELO(self, server, session, envelope, hostname):
        print("HELO received with hostname:", hostname)
        return '250 Hello {}'.format(hostname)

    async def handle_EHLO(self, server, session, envelope, hostname):
        print("EHLO received with hostname:", hostname)
        return '250-Hello {}\n250-STARTTLS\n250 OK'.format(hostname)

    async def handle_MAIL(self, server, session, envelope, address, mail_options):
        print("MAIL FROM:", address)
        return '250 OK'

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        print("RCPT TO:", address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        print("DATA received")
        print('From:', envelope.mail_from)
        print('To:', envelope.rcpt_tos)
        print('Data:', envelope.content.decode())
        return '250 Message accepted for delivery'

    async def handle_RSET(self, server, session, envelope):
        print("RSET received")
        envelope.reset()
        return '250 OK'

    async def handle_NOOP(self, server, session, envelope):
        print("NOOP received")
        return '250 OK'

    async def handle_VRFY(self, server, session, envelope, address):
        print("VRFY received for:", address)
        return '252 Cannot VRFY user, but will accept message and attempt delivery'

    async def handle_EXPN(self, server, session, envelope, address):
        print("EXPN received for:", address)
        return '502 EXPN command not implemented'

    async def handle_QUIT(self, server, session, envelope):
        print("QUIT received")
        return '221 Bye'

    async def handle_STARTTLS(self, server, session, envelope):
        print("STARTTLS received")
        return '220 Ready to start TLS'

if __name__ == '__main__':
    controller = Controller(CustomSMTPHandler(), hostname='0.0.0.0', port=1025)
    controller.start()
    print("SMTP server running on port 1025")
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass

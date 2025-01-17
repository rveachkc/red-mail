
from email.message import EmailMessage
import pytest

from redmail import EmailSender, send_email

class MockServer:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.is_login = False

    def starttls(self):
        return

    def login(self, user=None, password=None):
        self.is_login = True
        return

    def send_message(self, msg):
        return

    def quit(self):
        return

def test_send():
    email = EmailSender(host="localhost", port=0, cls_smtp=MockServer)
    assert email.connection is None

    msg = email.send(
        subject="An example",
        receivers=['koli.mikael@example.com']
    )
    assert isinstance(msg, EmailMessage)
    assert email.connection is None

def test_send_multi():
    email = EmailSender(host="localhost", port=0, cls_smtp=MockServer)

    assert email.connection is None
    with email:
        assert email.connection is not None
        msg = email.send(
            subject="An example",
            receivers=['koli.mikael@example.com']
        )
        assert isinstance(msg, EmailMessage)
        assert email.connection is not None
        msg = email.send(
            subject="An example",
            receivers=['koli.mikael@example.com']
        )
        assert isinstance(msg, EmailMessage)
        assert email.connection is not None
    assert email.connection is None

def test_send_function():
    # This should fail but we test everything else goes through
    with pytest.raises(ConnectionRefusedError):
        send_email(host="localhost", port=0, subject="An example")
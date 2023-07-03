import smtplib
import socket
from email.message import EmailMessage
from email.utils import make_msgid

from mail_status import SendMailReturnErrorCode, print_error_message_and_exit


def send_email(smtp_server: str, smtp_credentials: str, imap_address: str):
    email_sent_successfully = False
    sent_email_id = None

    try:
        smtp_server_obj = smtplib.SMTP(smtp_server)
        username, password = smtp_credentials
        smtp_server_obj.login(username, password)

        from_addr = username
        to_addr = imap_address
        subject = "Test-E-Mail"
        body = "This is a test email"

        msg = EmailMessage()
        msg["From"] = from_addr
        msg["To"] = to_addr
        msg["Subject"] = subject
        msg.set_content(body)

        msg_id = make_msgid()
        msg["Message-ID"] = msg_id

        smtp_server_obj.send_message(msg)
        email_sent_successfully = True
        sent_email_id = msg_id

        smtp_server_obj.quit()

    except (smtplib.SMTPAuthenticationError, smtplib.SMTPNotSupportedError) as ex:
        print_error_message_and_exit(
            SendMailReturnErrorCode.SMTP_CREDENTIAL_FAILED, [str(ex)]
        )
    except (smtplib.SMTPConnectError, socket.gaierror) as ex:
        print_error_message_and_exit(
            SendMailReturnErrorCode.SMTP_CONNECTION_FAILED, [str(ex)]
        )

    send_email.email_sent_successfully = email_sent_successfully
    send_email.sent_email_id = sent_email_id

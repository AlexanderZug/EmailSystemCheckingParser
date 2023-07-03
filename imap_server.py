import email
import imaplib
import time

from mail_status import (SendMailReturnErrorCode, SendMailReturnStatusMsg,
                         print_error_message_and_exit, print_message)
from smtp_server import send_email


def receive_email(
        imap_server: str,
        imap_credentials: str,
        timeout: float,
        warning_threshold: int,
):
    email_received_successfully = False

    try:
        imap_server_obj = imaplib.IMAP4_SSL(imap_server)
        username, password = imap_credentials
        imap_server_obj.login(username, password)
        imap_server_obj.select("INBOX")

        start_time = time.time()

        while True:
            response = imap_server_obj.noop()
            if response[0] == "OK":
                _, data = imap_server_obj.search(None, "ALL")
                msg_ids = data[0].split()

                if msg_ids:
                    latest_msg_id = msg_ids[-1]
                    _, msg_data = imap_server_obj.fetch(latest_msg_id, "(RFC822)")
                    msg = email.message_from_bytes(msg_data[0][1])
                    letter_id = msg["Message-ID"]

                    if (
                        hasattr(send_email, "sent_email_id")
                        and send_email.sent_email_id == letter_id
                    ):
                        email_received_successfully = True
                        break

                    imap_server_obj.store(latest_msg_id, "+FLAGS", "\\Deleted")
                    imap_server_obj.expunge()

            elapsed_time = time.time() - start_time
            if elapsed_time > timeout and hasattr(send_email, "sent_email_id"):
                print_error_message_and_exit(
                    SendMailReturnErrorCode.TIMEOUT_ERROR,
                    [f"Timeout error: {elapsed_time}"],
                )

            if time.time() - start_time > warning_threshold and hasattr(send_email, "sent_email_id"):
                print_message(SendMailReturnStatusMsg.transfer_time_warning)

        imap_server_obj.logout()

    except imaplib.IMAP4.error as ex:
        print_error_message_and_exit(
            SendMailReturnErrorCode.IMAP_CREDENTIAL_FAILED,
            [str(ex)],
        )
    except IOError as ex:
        print_error_message_and_exit(
            SendMailReturnErrorCode.IMAP_CONNECTION_FAILED,
            [str(ex)],
        )

    receive_email.email_received_successfully = email_received_successfully

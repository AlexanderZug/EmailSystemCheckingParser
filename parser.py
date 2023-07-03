import argparse
import threading
import time

from imap_server import receive_email
from mail_status import SendMailReturnStatusMsg, print_message
from smtp_server import send_email


def get_cli_options() -> argparse.Namespace:
    """
    Return CLI argument object
    """
    parser = argparse.ArgumentParser(
        description="Check proxy for proving email sending and receiving."
    )
    parser.add_argument(
        "--imap-server",
        type=str,
        required=True,
        help="IMAP server address",
    )
    parser.add_argument(
        "--smtp-server",
        type=str,
        required=True,
        help="SMTP server address",
    )
    parser.add_argument(
        "--imap-credentials",
        type=str,
        nargs="+",
        required=True,
        help="IMAP credentials: username password",
    )
    parser.add_argument(
        "--smtp-credentials",
        type=str,
        nargs="+",
        required=True,
        help="SMTP credentials: username password",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60,
        help="Timeout for IMAP idle check",
    )
    parser.add_argument(
        "--warning-threshold",
        type=int,
        default=10,
        help="Warning threshold for email delivery duration",
    )
    return parser.parse_args()


def main():
    options = get_cli_options()

    imap_thread = threading.Thread(
        target=receive_email,
        args=(
            options.imap_server,
            options.imap_credentials,
            options.timeout,
            options.warning_threshold,
        ),
    )

    imap_thread.start()

    time.sleep(2)

    smtp_thread = threading.Thread(
        target=send_email,
        args=(
            options.smtp_server,
            options.smtp_credentials,
            options.imap_credentials[0],
        ),
        daemon=True,
    )

    smtp_thread.start()
    # Wait for the email to be sent
    smtp_thread.join()

    if (
        hasattr(send_email, "email_sent_successfully")
        and send_email.email_sent_successfully
    ):
        stopwatch_start = time.time()
        print_message(SendMailReturnStatusMsg.email_sent)

    # Wait for the response email and check its content
    imap_thread.join()

    if (
        hasattr(receive_email, "email_received_successfully")
        and receive_email.email_received_successfully
    ):
        print_message(SendMailReturnStatusMsg.email_recieved)


if __name__ == "__main__":
    main()

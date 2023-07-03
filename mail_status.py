import os
from dataclasses import dataclass
from enum import Enum
from typing import List


class SendMailReturnErrorCode(Enum):
    SMTP_CONNECTION_FAILED = 1
    IMAP_CONNECTION_FAILED = 2
    SMTP_CREDENTIAL_FAILED = 3
    IMAP_CREDENTIAL_FAILED = 4
    TIMEOUT_ERROR = 5
    SENT_FAILED = 6
    RECIEVED_FAILED = 7


@dataclass
class SendMailReturnStatusMsg:
    email_sent: str = "Successfully sent"
    email_recieved: str = "Successfully received"
    transfer_time_warning: str = "Timeout warning"


def print_error_message_and_exit(
    status: SendMailReturnErrorCode,
    messages: List[str],
):
    print("{}: {}".format(status.name, "".join(messages)))
    os._exit(status.value)


def print_message(mail_status: str):
    print(mail_status)

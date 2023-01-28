import os


def get_default_logger_path() -> os.path:
    logs_path = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    return logs_path

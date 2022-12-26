import config.config as config

file_name = "log.txt"
write_to_file = False


def log(log_info):
    print(log_info)
    if write_to_file:
        __write_to_file(log_info)


def __write_to_file(log_info):
    file = open(file_name, "a")
    file.write(log_info + "\n")
    file.seek(0, 2)
    size = file.tell()
    file.close()
    if size > config.LOG_SIZE_LIMIT_BYTES:
        __enforce_size_limit()


def __enforce_size_limit():
    file = open(file_name, "w")
    file.seek(config.LOG_SIZE_LIMIT_BYTES, 2)
    file.write(file.read())
    file.close()

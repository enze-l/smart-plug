file_name = "log_history.txt"
limit = 4096


def log(log_info):
    print(log_info)
    file = open(file_name, "a")
    file.write(log_info + "\n")
    file.seek(0, 2)
    size = file.tell()
    file.close()
    if size > limit:
        __enforce_size_limit()


def __enforce_size_limit():
    file = open(file_name, "w")
    file.seek(limit, 2)
    file.write(file.read())
    file.close()

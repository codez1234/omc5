from datetime import date, datetime
import os


def time_now():
    now = datetime.now()
    return str(now)


def date_now():
    today = date.today()
    Str = date.isoformat(today)
    return Str


def parent_dir():
    # print(os.getcwd())
    return os.getcwd()


def request_text_file(user=None, value=None):
    file_path = f'{parent_dir()}/logFiles/request/{date_now()}.txt'
    # print(f'file_path == {file_path}')
    try:
        with open(file_path, "a") as f:
            f.write("\n")
            f.write(time_now())
            f.write("\n")
            f.write(f'user id is {str(user)}')
            f.write("\n")
            f.write(str(value))
            f.write("\n")

    except FileNotFoundError:
        print("The 'docs' directory does not exist")


def response_text_file(user=None, value=None):
    file_path = f'{parent_dir()}/logFiles/response/{date_now()}.txt'
    # print(f'file_path == {file_path}')
    try:
        with open(file_path, "a") as f:
            f.write("\n")
            f.write(time_now())
            f.write("\n")
            f.write(f'user id is {str(user)}')
            f.write("\n")
            f.write(str(value))
            f.write("\n")

    except FileNotFoundError:
        print("The 'docs' directory does not exist")


'''
dic = {"ram": 1,
       "ral": 444,
       "kjsdjfs": 66}

text_file(value=dic)

'''

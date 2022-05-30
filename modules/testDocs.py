# from datetime import date


# def get():
#     today = date.today()
#     # Converting the date to the string
#     Str = date.isoformat(today)
#     # print("String Representation", Str)
#     return Str


'''

# Python program to
# print current date

from datetime import date

# calling the today
# function of date class
today = date.today()

print("Today's date is", today)
'''

'''
from datetime import date

# calling the today
# function of date class
today = date.today()

# Converting the date to the string
Str = date.isoformat(today)
print("String Representation", Str)
print(type(Str))
'''
'''

def date_now():
    today = date.today()
    # Converting the date to the string
    Str = date.isoformat(today)
    # print("String Representation", Str)
    return Str


def fn():
    print(os.getcwd())
    return os.getcwd()


# flle_dir = fn()

file_path = f'{fn()}/modules/short.txt'

with open(file_path, "a") as rf:
    x = rf.write("ok\n")
    print(x)

# /home/shubham/Desktop/omc-api/omc-auth_api-test3
# 'x' open for exclusive creation, failing if the file already exists
with open(file_path, "a") as rf:
    x = rf.write("ok2\n")
    y = rf.write("ok3\n")
    print(x)

'''

'''
try:
    with open('docs/readme.txt', 'w') as f:
        f.write('Create a new text file!')
except FileNotFoundError:
    print("The 'docs' directory does not exist")
'''

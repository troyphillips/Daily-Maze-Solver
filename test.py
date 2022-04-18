import datetime

with open("test.txt","w") as file:
    str = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    file.write(str)
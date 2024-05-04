import os

SEPORATOR = ""

def read(name):
    file = open(name, "r")
    read = file.read()
    file.close()
    return read

def write(name, text):
    file = open(name, "w")
    file.write(text)
    file.close()
    
def append(name, text):
    file = open(name, "a")
    file.write(text)
    file.close()

def table_read(name):
    list = []

    file = open(name)
    read = file.read()
    file.close()

    while read != " " and read != "":
        list.append(read[:read.find(SEPORATOR)])
        read = read[read.find(SEPORATOR)+1:]
    
    return list

def table_write(name, list):
    text_string = ''

    if len(list) <= 0:
        return False

    for element in list:
        text_string = text_string + str(element) + SEPORATOR
    
    file = open(name, "w")
    file.write(text_string)
    file.close()

def table_append(name,list):
    text_string = ''

    if len(list) <= 0:
        return False

    for element in list:
        text_string = text_string + str(element) + SEPORATOR

    file = open(name,"a")
    file.write(text_string)
    file.close()

def remove(name):
    if os.path.exists(name):
        os.remove(name) 

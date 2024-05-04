def root(num, root=2.0):
    num = float(num) ** (1.0/root)
    if str(num)[len(str(num))-2:] == ".0":
        num = int(num)
    return num

def prime(num):
    if int(num) != num:
        exit("Expected `int` with `prime()`")

    if num < 2:
        return False
    
    for div in range(2,int(num/2)+1):
        if num % div == 0:
            return False
        
    return True

def prime_list(startNum, endNum):

    if startNum != int(startNum) or endNum != int(endNum):
        exit("Expected `int` with `prime_list()`")

    list = []
    for i in range(startNum, endNum+1):
        if prime(i):
            list.append(i)
    
    return list

def factorial(num):
    if num != int(num):
        exit("Expected `int` with `factorial()`")

    endNum = 1
    while num > 0:
        endNum *= num
        num -= 1
    return endNum

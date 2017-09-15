import csv


def alphaToInt(string):
    num = 0;
    l = 16 ** (len(string) - 1)
    for i in range(len(string)):
        if string[i] == 'a':
            num += 10 * l
        elif string[i] == 'b':
            num += 11 * l
        elif string[i] == 'c':
            num += 12 * l
        elif string[i] == 'd':
            num += 13 * l
        elif string[i] == 'e':
            num += 14 * l
        elif string[i] == 'f':
            num += 15 * l
        else:
            num += int(string[i]) * l
        l //= 10
    return num


def makeHeader(list):
    new_list = []
    for element in list:
        my_element = element.split('\\x')[1:]
        tmp_element = my_element[len(my_element) - 1][:2]
        my_element = my_element[:][:len(my_element) - 1]
        my_element.append(tmp_element)
        for i in range(len(my_element)):
            my_element[i] = alphaToInt(my_element[i])
        new_list.append(bytearray(my_element).decode())

    return new_list


def readCSV(filename):
    f = open(filename, 'r', encoding='utf-8')
    reader = csv.reader(f)
    arr = []
    sw = True
    for line in reader:
        if sw:
            arr.append(makeHeader(line))
            sw = False
        else:
            arr.append(line)
    f.close()
    return arr


file = readCSV('/Users/jiharu/Desktop/2016년도 수학가형 수능 등급컷.csv')
print(file)

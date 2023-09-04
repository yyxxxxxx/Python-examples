with open("file_to_read.txt", "r") as file1:
    content = file1.readline()
    list = content.split()
    num = 0
    for items in list:
        if "terrible" in items:
            num = num + 1
    print(f"The total number of 'terrible' is {num}")

with open("result.txt", "w") as file2:
    cnt = 1
    for items in list:
        if "terrible" in items:
            if cnt % 2 == 0:
                pos = list.index(items)
                str = items.replace("terrible","pathetic")
                list.remove(items)
                list.insert(pos,str)
                cnt = cnt + 1
            elif cnt % 2 == 1:
                pos = list.index(items)
                str = items.replace("terrible", "marvellous")
                list.remove(items)
                list.insert(pos,str)
                cnt = cnt + 1
    str = " ".join(list)
    file2.write(str)
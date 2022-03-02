with open("list.txt", "r") as file:
    contents = file.read()
l1 = contents.split(sep = '\n', maxsplit = 1)

list_w = l1[0].split(sep = ',')
list_m = l1[1].split(sep = ',')

print(l1)
print(list_w)
print(list_m)
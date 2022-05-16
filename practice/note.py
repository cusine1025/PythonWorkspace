def myfunct(argument, keyword = 0, *args,**kwargs):
    
    print('argument: ',argument)
    print('keyword: ', keyword)
    print("args: ", args)
    print("kwargs: ", kwargs)
 
myfunct('hi', 'geeks','for','geeks',first="Geeks",mid="for",last="Geeks")


square = lambda x: x * x
print(square(2))
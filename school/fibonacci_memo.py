dictionary = {
    1: 1,
    2: 2
}
counter = 0

def fibonacci(n):
    if n in dictionary:
        return dictionary[n]
    else:
        output = fibonacci(n - 1) + fibonacci(n - 2)
        global counter
        counter += 1
        dictionary[n] = output
        return output

print("fibonacci(20):", fibonacci(20))
print("fibonacci 계산에 활용된 덧셈 횟수 : {}번".format(counter))

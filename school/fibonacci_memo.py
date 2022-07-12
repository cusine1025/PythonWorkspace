# 메모 변수를 만듭니다.
dictionary = {
    1: 1,
    2: 2
}
counter = 0
global count
# 함수를 선언합니다.
def fibonacci(n):
    if n in dictionary:
        # 메모 되어 있으면 메모된 값 리턴
        return dictionary[n]
    else:
        # 메모 되어 있지 않으면 값을 구함
        output = fibonacci(n - 1) + fibonacci(n - 2)
        global counter
        counter += 1
        dictionary[n] = output
        return output

# 함수를 호출합니다.

print("fibonacci(50):", fibonacci(20))
print("fibonacci 계산에 활용된 덧셈 횟수는 {}번입니다.".format(counter))

n,k = input().split(' ')
n = int(n)
k = int(k)
row = []

for row_index in range(n):
    row.append([])
    row[row_index].append('.' * n)


not_counted_yes = 0

while not_counted_yes == 0:
    pass

# 가로줄 검출하기
for row_index in range(n):
    if row[row_index].count('#') != n:
        not_counted_yes = 'yes'

# 세로줄 검출하기
for list_index in range(n):
    for row_index in range(n):
        if row[row_index][list_index] != '#':
            not_counted_yes = 'yes'

# 대각선 (왼쪽 상단 -> 오른쪽 하단) 검출하기
for row_index in range(n):
    if row[row_index][row_index] != '#':
        not_counted_yes = 'yes'

# 대각선 (오른쪽 상단 -> 왼쪽 하단) 검출하기
for row_index in range(n):
    if row[row_index][n-row_index] != '#':
        not_counted_yes = 'yes'

bingo = 0



print
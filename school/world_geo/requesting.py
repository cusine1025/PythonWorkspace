import requests
import json
from openpyxl import Workbook

# 엑셀 만들기
write_wb = Workbook()
write_ws = write_wb.create_sheet('세계지리통계')
write_ws = write_wb.active

# Open API에 인증키와 비밀키를 입력하여 자료요청에 필요한 엑세스 토큰을 얻기
consumer_key = ''
consumer_secret = ''
data = requests.get('https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json'
    + '?' + 'consumer_key=' + consumer_key + '&consumer_secret=' + consumer_secret)
contents = data.text
json_ob = json.loads(contents)

# 토큰 변수 정의
access_token = json_ob['result']['accessToken']

# 토큰을 이용하여 인구수 조사 통계 가져오기
pop_data = requests.get('https://sgisapi.kostat.go.kr/OpenAPI3/stats/searchpopulation.json'
    + '?' + 'accessToken=' + access_token + '&year=2020')
pop_contents = pop_data.text
json_pop = json.loads(pop_contents)

# 통계 데이터를 리스트에 넣기
place = []
for i in range(14):
    place.append(list(json_pop['result'][i].values()))

# 기준표 먼저 출력
write_ws.append(['설명', '행정구역명', '검색인구 평균나이', '인구수'])

# 데이터 입력
for i in range(14):
    write_ws.append(place[i])

# 저장
write_wb.save('세계지리 통계표.xlsx')
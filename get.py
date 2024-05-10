
import requests

url = 'http://localhost:3000/wanted'

response = requests.get(url)
if response.status_code == 200:
    print('요청이 성공했습니다.')
    print('응답 데이터:', response.text)
else:
    print('요청이 실패했습니다. 상태 코드:', response.status_code)

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# POST 요청을 처리하는 핸들러 클래스
class PostRequestHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # 전송된 데이터의 길이 가져오기
        post_data = self.rfile.read(content_length)  # 전송된 데이터 읽기
        post_data_str = post_data.decode('utf-8')  # 바이너리 데이터를 문자열로 디코딩
        
        # 전송된 데이터 출력
        print("Received POST data:")
        print(post_data_str)

        # 클라이언트에게 응답 보내기
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'Received POST data'}).encode())

# 서버 설정
host = 'localhost'
port = 8000

# 서버 시작
server = HTTPServer((host, port), PostRequestHandler)
print(f'Server started on {host}:{port}')

# 서버 실행
server.serve_forever()

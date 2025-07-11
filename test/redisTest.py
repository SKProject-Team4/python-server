import redis

def test_redis_connection():
    try:
        # Redis 서버에 연결 (기본 설정: localhost, 포트 6379)
        r = redis.Redis(host='219.255.15.170', port=6383, db=0)

        # 테스트용 key-value 설정
        r.set('test_key', 'Hello, Redis!')

        # 값 가져오기
        value = r.get('test_key')

        print("Redis에서 가져온 값:", value.decode('utf-8'))

    except redis.exceptions.ConnectionError as e:
        print("Redis 연결 실패:", e)

if __name__ == "__main__":
    test_redis_connection()
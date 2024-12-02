# Weave - BE
Project Weave: 동아리 종합지원 관리서비스

## A. How to Run

> Docker를 사용하는 방법과 사용하지 않는 방법으로 2가지 경우를 정리해두었습니다.
상황에 따라 적절히 선택해 테스트하시기 바랍니다.

### case1: Docker로 테스트

로컬환경에서 테스트할 때는 가능한 docker환경을 권장합니다.

#### 0. git clone & 환경변수 추가

git을 clone한 후, 공유된 env를 프로젝트 최상단에 `.env`라는 파일을 만들어 저장합니다

#### 1. Docker 이미지 빌드

Dockerfile이 위치한 디렉터리에서 아래 명령어를 실행하여 이미지를 빌드합니다:

```bash
docker build --env-file .env -t weave_be_image .
```

`weave_be_image`는 이미지 이름입니다.


#### 2. Docker 컨테이너 실행

빌드된 이미지를 기반으로 컨테이너를 실행합니다:

```bash
docker run -d -p 8000:8000 --name weave_be weave_be_image
```

- -d: 백그라운드 모드로 실행.
- -p 8000:8000: 호스트와 컨테이너의 포트를 매핑.
- --name weave_be: 컨테이너 이름 지정.


### case2: python venu환경에서 실행

docker 사용이 불가한 경우 로컬환경에서 venu init을 통해 실행합니다

#### 0. git clone & 환경변수 추가

case1과 동일합니다

#### 1. 가상환경 생성 및 활성화

```bash
python3 -m venv venv

source venv/bin/activate # for linux/mac
venv\Scripts\activate # for Windows
```

#### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

#### 3. 서버 실행

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

콘솔에 다음과 같이 표시되면 서버가 정상적으로 실행 중이라는 뜻입니다:

```shell
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
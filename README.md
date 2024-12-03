# Weave - BE
Project Weave: 동아리 종합지원 관리서비스

## A. 시작하기 앞서

- 모든 작업은 반드시 `dev/[사용자_닉네임]` branch에서 작업 후 main으로 merge 주셔야 합니다
  - git push 하셔도 ruleset 걸어둬서 안됩니다.
- Git Message Convention은 권장드리지만, 시간제한 상 **강제하지 않겠습니다**
- Git PR Convention은 적용을 권장드립니다. 아래 양식을 참고하여 PR 부탁드립니다
  - 제목예시: `Feat: TestAPI Gateway 추가`
  - 형식:
    ```markdown
      # Feat: TestAPI Gateway 추가
      ---

      ## 주요 수정사항
      - 수정사항을 목록으로 작성
      - 간단하게만 언급
      - 우측 'Reviewers'에 팀원들 선택
      - 'Assignees'에는 본인 선택
      - PR 올리고 카톡으로도 알려주기!
    ```
- publish로 올라가는 PR은 merge 즉시 자동배포됩니다. 아직 설정이 완벽하지 않아서, 이건 완료되는대로 다시 공유하겠습니다

## B. Architecture

FastAPI를 협업하기 가장 좋은 형태로 사용하기 위해, Architecture는 MVC패턴을 계층형 기반으로 적절히 수정하여 적용하였습니다.
각 폴더는 다음과 같은 역할을 수행합니다

```bash
/app
  
 ㄴ /apis: API도메인 별 디렉토리
 ㄴ /common: API도메인 간 공통으로 사용되는 코드를 저장하는 디렉토리
 ㄴ /middlewares: middlware 로직 디렉토리
  
 ㄴ config.py: .env parsing 파일
 ㄴ db.py: DB Query전달 및 응답처리 함수를 담당하는 파일
 ㄴ main.py: FastAPI 서버생성 및 flow handling 파일

/logs: 로그저장 디렉토리 (내부에 파일이 자동으로 생성됩니다)
```

`/apis` 내에 저장되는 API 도메인은 다음과 같이 구성되어 있습니다:

```bash
/[DOMAIN_NAME]

 ㄴ /repository: db 접근관련 로직 디렉토리
  ㄴ query.py: 과목과제 보고서를 위한 파일; 상수형태로 DB Query 관리
  ㄴ repository.py: query.py에서 상수형태의 query를 가져와 실행

 ㄴ /service: repository 내의 함수에서 데이터를 받아 원하는 형식으로 가공하는 로직을 관리하는 디렉토리
  ㄴ [적절한_이름별로_구분된_service_파일명].py

 ㄴ /router: service 내의 함수에서 결과를 받아 요청을 직접 처리하는 코드를 담은 디렉토리
  ㄴ router.py: service 내의 함수에서 결과를 받아 요청을 직접 처리
```

## C. How to Run

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
python -m app.main
```

콘솔에 다음과 같이 표시되면 서버가 정상적으로 실행 중이라는 뜻입니다:

```shell
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

<a href="https://docs.docker.com/guides/docker-concepts/the-basics/what-is-a-container/" target="_blank">@[도커 공식 문서 바로가기]</a>
# Container
* 컨테이너는 가상화 기술의 한 형태로, 소프트웨어 애플리케이션을 실행하기 위한 표준화된 환경을 제공한다.
* 각 컨테이너는 소프트웨어 애플리케이션에 필요한 환경을 포함하며, 각 애플리케이션에 독립적인 프로세스이다.
* 호스트 시스템의 운영 체제 커널을 공유하면서 격리된 환경을 제공하며, 가상머신(VM) 비교해 더 가볍고 효율적이다. 
* 컨테이너는 Docker, Kubernetes 등의 도구를 사용하여 관리된다.

## Docker
**Docker Engine = Docker Server(docker daemon) + Docker Client**
로컬 머신에서 실행되고 있는 dockerd에서 도커 명령어를 모니터링 한다


도커 엔진 설치 후 자동으로 도커 데몬이 설치되지만 수동으로 실행하려면 아래 명령어를 입력한다.
```sh
# 데비안,우분투
sudo systemctl start docker
```

## DockerFile
### 이미지 만들기
| Instruction  | Description |
|---:|:---|
|**ADD**| Add local or remote files and directories.  |
|**ARG**|Use build-time variables.|
|**CMD**|Specify default commands.|
|**COPY**|Copy files and directories.|
|**ENTRYPOINT**|Specify default executable.|
|**ENV**|Set environment variables.|
|**EXPOSE**|Describe which ports your application is listening on.|
|**FROM**|Create a new build stage from a base image.|
|**HEALTHCHECK**|Check a container's health on startup.|
|**LABEL**|Add metadata to an image.|
|**MAINTAINER**|Specify the author of an image.|
|**ONBUILD**|Specify instructions for when the image is used in a build.|
|**RUN**|Execute build commands.|
|**SHELL**|Set the default shell of an image.|
|**STOPSIGNAL**|Specify the system call signal for exiting a container.|
|**USER**|Set user and group ID.|
|**VOLUME**|Create volume mounts.|
|**WORKDIR**|Change working directory.|

#### DockerFile 작성하고 빌드하기
requirements.txt
```
Flask==2.1.0
pandas==0.25.2
Flask-HTTPAuth==3.3.0
click==8.0
numpy==1.23.1
Werkzeug==2.0.0
```

```sh
# 기반 이미지 정의
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt .

# 의존성 설치
RUN pip install -r requirements.txt

# 소스 코드 복사
COPY . .

# 컨테이너가 실행될 명령 설정
CMD ["python", "app.py"]
```

```sh
docker build -t $image:$tag $PATH
```


## Docker 사용하기
### docker 명령어
|명령어|옵션|설명|비고|
|:---------|:---|:---|:-------------|
|ps| ||```docker ps```|
||-a|실행중이지 않은 도커 컨테이너 리스트까지 확인하기|```docker ps -a```|
|images||도커 이미지 조회하기|```docker images```|
|run||docker pull + docker create + docker start|```docker run -d --name $name -p $hostp:$containerp -v $hostv:$containerv $image```|
||name|컨테이너 이름 지정||
||d|컨테이너를 백그라운드에서 실행 --detach||
||v|호스트와 컨테이너 간의 볼륨 연결||
||p|호스트와 컨테이너 간의 포트 연결||
|exec|||```docker exec -it $container bash```|
||i|--interactive||
||t|--tty||
|network||||
||ls||```docker network ls```|
|inspect|||```docker inspect $container```|
|logs|||```docker logs $container```|
|stop|||```docker stop $container```|
|rm|||```docker rm $container```|
|save|o||```docker save -o $name.tar $image:$tag```|
|load|i||```docker load -i $name.tar```|

#基础镜像为debian build镜像时会自动下载
FROM python:3.9.2 
 
#制作者信息
LABEL MAINTAINER=chace.min@qq.com
 
#设置环境变量
ENV CODE_DIR=/opt
ENV DOCKER_SCRIPTS=$CODE_DIR/Industriallog
 
#将scripts下的文件复制到镜像中的DOCKER_SCRIPTS目录
#设置国内源
COPY ./sources.list /etc/apt/sources.list

ADD ./crontab /etc/cron.d/crontab
COPY ./*.py $DOCKER_SCRIPTS/
COPY ./requirements.txt $DOCKER_SCRIPTS/
COPY ./sources.list $DOCKER_SCRIPTS/
COPY ./run.sh $DOCKER_SCRIPTS/

#安装软件
RUN apt-get update -y && apt-get install -y vim && apt-get install -y cron && touch /var/log/cron.log

# 赋于运行权限
RUN chmod 0644 /etc/cron.d/crontab
# 运行任务
RUN crontab /etc/cron.d/crontab



# 设置国内镜像源
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
# 安装更新
RUN pip install --upgrade pip
# 设置权限
RUN chmod 777 $DOCKER_SCRIPTS/*
# 安装支持
RUN pip install -r $DOCKER_SCRIPTS/requirements.txt
 
#执行镜像中的provision.sh脚本

RUN echo "hello world"
# 一直跑
CMD ["cron", "-f"]

#基础镜像为debian build镜像时会自动下载
FROM python:3.9.2 
 
#制作者信息
LABEL MAINTAINER=chace.min@qq.com
 
#设置环境变量
ENV CODE_DIR=/opt
ENV DOCKER_SCRIPTS=$CODE_DIR/Industriallog
 
#将scripts下的文件复制到镜像中的DOCKER_SCRIPTS目录
COPY ./* $DOCKER_SCRIPTS/

# 设置国内镜像源
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
# 安装更新
RUN pip install --upgrade pip
# 设置权限
RUN chmod 777 $DOCKER_SCRIPTS/*
# 安装支持
RUN pip install -r $DOCKER_SCRIPTS/requirements.txt
 
#执行镜像中的provision.sh脚本

#RUN $DOCKER_SCRIPTS/Deal_name_mtr.py
#RUN $DOCKER_SCRIPTS/run.sh
RUN echo "hallo word"

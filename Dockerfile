# 基础镜像，官方lts版本
FROM jenkins/jenkins:latest
# 切换root用户执行系统安装
USER root
#0. 备份原来的镜像源
RUN cp /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list.d/debian.sources.bak
# 1.替换Debian trixie清华源 DEB822格式
# 1.替换Debian trixie清华源，使用printf写入，不使用heredoc
RUN printf 'Types: deb\nURIs: https://mirrors.tuna.tsinghua.edu.cn/debian\nSuites: trixie trixie-updates\nComponents: main contrib non-free non-free-firmware\nSigned-By: /usr/share/keyrings/debian-archive-keyring.gpg\n\nTypes: deb\nURIs: https://mirrors.tuna.tsinghua.edu.cn/debian-security\nSuites: trixie-security\nComponents: main contrib non-free non-free-firmware\nSigned-By: /usr/share/keyrings/debian-archive-keyring.gpg\n' > /etc/apt/sources.list.d/debian.sources


#2. 安装python pip
RUN  apt-get clean  \
&& apt-get update \
     && apt-get install -y python3-full \
     python3-pip  \
     unzip  \
     curl \
     ca-certificates


## 3.下载安装 allure‑commandline，可修改ALLURE_VERSION修改版本
#ARG ALLURE_VERSION=2.44.1
#RUN curl -fsSL https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.zip -o /tmp/allure.zip \
#&& unzip -q /tmp/allure.zip -d /usr/local/src/ \
#    && mv /usr/local/src/allure-${ALLURE_VERSION} /usr/local/src/allure \
#    && chmod -R 777 /usr/local/src/allure \
#    && rm -f /tmp/allure.zip

# ==========本地COPYallure压缩包，不走github网络==========
COPY allure-2.44.1.zip /tmp/allure.zip
RUN unzip -q /tmp/allure.zip -d /usr/local/src/ \
    && mv /usr/local/src/allure-2.44.1  /usr/local/src/allure \
    && chmod -R 777 /usr/local/src/allure \
    && rm -f /tmp/allure.zip

# 4.全局环境变量，所有shell都生效（关键！不写.bashrc）
# 4.全局环境变量，合并PATH；jenkins/jenkins:lts镜像运行时自带JAVA_HOME=/opt/java/openjdk
ENV PATH="/usr/local/src/allure/bin:${JAVA_HOME}/bin:${PATH}"

# 设置容器启动后的默认运行目录
WORKDIR /usr/local
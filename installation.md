# 说明文档

## 一　运行环境及使用框架

    Ubuntu 16
    python >= 3.5
    node v12.9.1
    npm 6.11.2
    vuejs

    后端：django
    前端：element ui + vuejs

## 二　环境搭建

### 安装django

    pip install django

### 安装vue以及所需启动前端

    npm install --global vue-cli
    cd frontend/
    npm install

### 安装mysql
    sudo apt install mysql-server

    mysql -uroot -p （密码设置为123456）

    CREATE DATABASE ImageProcessDatabase CHARACTER SET utf8;

### 安装深度学习所需要的库

    sudo pacman -S cmake

    pip install face-recognition
    pip install pymysql
    pip install django-core-headers

    pip install scikit-image --user
    pip install torchvision --user
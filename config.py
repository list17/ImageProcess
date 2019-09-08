#-*- coding:utf-8 -*-
#该项目的第三方配置


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "ImageProcessDatabase",
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;"
        }
    }
}

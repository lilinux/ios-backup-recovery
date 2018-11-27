#!/bin/bash

echo 'init start'
yum install -y python-pip python-devel gcc openssl-devel
pip install -i http://mirrors.tencentyun.com/pypi/simple --trusted-host mirrors.tencentyun.com fastpbkdf2 pycrypto
echo 'init finish'

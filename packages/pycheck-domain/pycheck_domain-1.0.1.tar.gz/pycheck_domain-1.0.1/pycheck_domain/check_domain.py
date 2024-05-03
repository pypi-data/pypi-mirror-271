# -*- coding: utf-8 -*-
# @Author : buyfakett
# @Time : 2023/12/28 11:26
import dns.resolver
import OpenSSL.crypto
from datetime import datetime


def check_domain(domain):
    """
    检测域名是否做了dns解析
    :param domain:      域名
    :return:            bool
    """
    try:
        dns.resolver.query(domain, 'A')
        return True
    except dns.resolver.NXDOMAIN:
        return False


def check_ssl(cert_file):
    """
    检测ssl证书的开始日期和到期日期
    :param cert_file: 文件路径
    :return: 开始日期和到期日期
    """
    # 读取证书文件
    with open(cert_file, 'r') as f:
        cert_data = f.read()

    # 使用OpenSSL加载证书
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_data)

    # 获取证书的开始和结束日期，并转换为datetime对象
    not_valid_before = datetime.strptime(cert.get_notBefore().decode('utf-8'), '%Y%m%d%H%M%SZ')
    not_valid_after = datetime.strptime(cert.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ')

    # 将日期格式化为yyyy-mm-dd
    formatted_not_valid_before = not_valid_before.strftime('%Y-%m-%d')
    formatted_not_valid_after = not_valid_after.strftime('%Y-%m-%d')

    return formatted_not_valid_before, formatted_not_valid_after

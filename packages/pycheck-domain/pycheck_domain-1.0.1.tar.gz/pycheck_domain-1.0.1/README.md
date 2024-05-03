<h1 align="center">pycheck_domain</h1>

- check_domain.py

检测域名是否做了dns解析，使用示例：

```python
if not check_domain(domain):
	return resp_400()
else:
	return resp_200()
```

检测ssl证书的开始时间和到期时间，使用示例：

```python
start_time, end_time = check_ssl(domain_path)
```

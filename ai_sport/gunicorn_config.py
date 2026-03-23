# Gunicorn 配置文件

# 绑定的 IP 和端口
bind = '127.0.0.1:8000'

# 工作进程数
workers = 4

# 工作进程类型
worker_class = 'gthread'

# 线程数
threads = 2

# 超时时间
timeout = 30

# 日志级别
loglevel = 'info'

# 日志文件路径
accesslog = './logs/gunicorn_access.log'
errorlog = './logs/gunicorn_error.log'

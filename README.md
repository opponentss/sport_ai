# 健身打卡软件

基于 Django 的健身打卡应用，支持以下功能：

- 打卡记录：记录健身活动，支持定位功能
- 三餐记录：记录饮食情况，支持拍照和AI营养分析功能
- 作息记录：记录睡眠情况，分析睡眠质量

## 技术栈

- Django 5.x
- PostgreSQL/SQLite
- Redis（缓存）
- Gunicorn（WSGI服务器）
- Nginx（反向代理）

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行迁移
python manage.py migrate

# 创建管理员账户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

## 部署

### 使用 Gunicorn 和 Nginx

1. 安装 Gunicorn：`pip install gunicorn`
2. 配置 Nginx（参考 nginx.conf）
3. 启动 Gunicorn：`gunicorn -c gunicorn_config.py ai_sport.wsgi`

## GitHub 推送命令

如果需要将代码推送到 GitHub，请在项目目录下运行以下命令：

```bash
git remote set-url origin https://github.com/opponentss/sport_ai.git
git push -u origin main
```

首次推送可能需要输入 GitHub 用户名和密码，或者使用 Personal Access Token。

## 功能说明

### AI 食物识别

在添加三餐记录时，可以上传食物图片并点击"AI 分析"按钮进行营养分析。

注意：目前使用的是模拟数据，实际使用需要配置真实的食物识别 API。

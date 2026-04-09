# 如何判断项目是否连接到PostgreSQL数据库

## 当前项目状态分析

基于对 `ai_sport` 项目的检查，以下是当前数据库连接状态：

### 1. 数据库配置分析
- **配置文件**: `ai_sport/ai_sport/settings.py`
- **配置逻辑**: 
  - 如果环境变量 `DATABASE_URL` 存在 → 使用 PostgreSQL
  - 如果不存在 → 使用 SQLite（默认）

### 2. 当前实际状态
- ✅ **数据库引擎**: `django.db.backends.sqlite3`
- ✅ **数据库文件**: `H:\ai_sport\ai_sport\db.sqlite3`
- ❌ **是否使用PostgreSQL**: 否
- ❌ **环境变量DATABASE_URL**: 未设置
- ✅ **数据库连接**: 正常（SQLite连接成功）

### 3. PostgreSQL服务状态
- ✅ **PostgreSQL客户端**: 已安装 (`H:\postgresql\bin\psql.exe`)
- ✅ **PostgreSQL服务**: 正在运行 (`postgresql-x64-18`)

## 判断项目是否连接到PostgreSQL的方法

### 方法1：检查Django设置
```python
# 检查当前数据库引擎
from django.conf import settings
db_engine = settings.DATABASES['default']['ENGINE']
is_postgresql = 'postgresql' in db_engine.lower()
print(f"使用PostgreSQL: {is_postgresql}")
print(f"数据库引擎: {db_engine}")
```

### 方法2：检查环境变量
```bash
# Windows
echo %DATABASE_URL%

# Linux/Mac
echo $DATABASE_URL
```

### 方法3：检查数据库连接详情
```python
# 检查连接详情
from django.db import connection
print(f"数据库后端: {connection.vendor}")
print(f"数据库版本: {connection.pg_version if hasattr(connection, 'pg_version') else 'N/A'}")
```

### 方法4：执行PostgreSQL特定查询
```python
# 尝试执行PostgreSQL特定查询
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version()")
        result = cursor.fetchone()
        print(f"PostgreSQL版本: {result[0]}")
except Exception as e:
    print(f"不是PostgreSQL或连接失败: {e}")
```

## 切换到PostgreSQL的步骤

### 步骤1：设置环境变量
```bash
# Windows
set DATABASE_URL=postgresql://username:password@localhost:5432/ai_sport_db

# 永久设置（系统属性）
```

### 步骤2：安装PostgreSQL适配器
```bash
pip install psycopg2-binary
```

### 步骤3：创建数据库
```sql
CREATE DATABASE ai_sport_db;
CREATE USER ai_sport_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ai_sport_db TO ai_sport_user;
```

### 步骤4：运行数据库迁移
```bash
python manage.py migrate
```

## 自动化检查脚本

创建一个检查脚本 `check_postgresql_connection.py`：

```python
#!/usr/bin/env python
import os
import sys
import django

def check_postgresql_connection():
    """检查项目是否连接到PostgreSQL数据库"""
    
    print("=== PostgreSQL连接检查 ===")
    
    # 1. 检查环境变量
    db_url = os.environ.get('DATABASE_URL')
    print(f"1. 环境变量DATABASE_URL: {'✅ 已设置' if db_url else '❌ 未设置'}")
    
    # 2. 检查Django设置
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_sport.settings')
    django.setup()
    
    from django.conf import settings
    db_engine = settings.DATABASES['default']['ENGINE']
    is_postgresql = 'postgresql' in db_engine.lower()
    
    print(f"2. 数据库引擎: {db_engine}")
    print(f"3. 使用PostgreSQL: {'✅ 是' if is_postgresql else '❌ 否'}")
    
    # 3. 测试数据库连接
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"4. 数据库连接: ✅ 成功")
            
            # 如果是PostgreSQL，检查版本
            if is_postgresql:
                cursor.execute("SELECT version()")
                pg_version = cursor.fetchone()[0]
                print(f"5. PostgreSQL版本: {pg_version}")
            else:
                print(f"5. 当前数据库: {connection.vendor}")
                
    except Exception as e:
        print(f"4. 数据库连接: ❌ 失败 - {e}")
    
    # 4. 总结
    print("\n=== 检查结果 ===")
    if is_postgresql:
        print("✅ 项目已连接到PostgreSQL数据库")
    else:
        print("❌ 项目未连接到PostgreSQL数据库")
        print("   当前使用: " + db_engine)
        
    return is_postgresql

if __name__ == "__main__":
    check_postgresql_connection()
```

## 常见问题排查

### 问题1：环境变量设置但未生效
- 检查终端会话是否重启
- 检查`.env`文件是否被正确加载
- 检查Django设置文件的加载顺序

### 问题2：PostgreSQL服务未运行
```bash
# 检查服务状态
sc query postgresql-x64-18

# 启动服务
net start postgresql-x64-18
```

### 问题3：连接权限问题
- 检查数据库用户权限
- 检查`pg_hba.conf`配置
- 检查防火墙设置

### 问题4：端口冲突
- 默认PostgreSQL端口：5432
- 检查端口是否被占用：`netstat -ano | findstr :5432`

## 结论

根据当前检查，**`ai_sport`项目未连接到PostgreSQL数据库**，而是使用SQLite作为默认数据库。

要切换到PostgreSQL，需要：
1. 设置`DATABASE_URL`环境变量
2. 安装`psycopg2-binary`包
3. 创建PostgreSQL数据库
4. 运行数据库迁移

项目已具备连接PostgreSQL的条件：
- ✅ PostgreSQL服务正在运行
- ✅ 项目配置支持PostgreSQL（通过环境变量切换）
- ✅ 代码结构兼容
#!/usr/bin/env python
"""
PostgreSQL连接检查脚本
用于判断Django项目是否连接到PostgreSQL数据库
"""

import os
import sys

def check_postgresql_connection():
    """检查项目是否连接到PostgreSQL数据库"""
    
    print("=" * 60)
    print("PostgreSQL数据库连接检查")
    print("=" * 60)
    
    results = {
        "environment_variable": False,
        "database_engine": False,
        "connection_test": False,
        "postgresql_service": False
    }
    
    # 1. 检查环境变量
    print("\n1. 检查环境变量DATABASE_URL:")
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        print(f"   [OK] 已设置: {db_url[:50]}..." if len(db_url) > 50 else f"   [OK] 已设置: {db_url}")
        results["environment_variable"] = True
    else:
        print("   [X] 未设置")
    
    # 2. 检查Django数据库配置
    print("\n2. 检查Django数据库配置:")
    try:
        # 添加项目路径
        sys.path.insert(0, 'ai_sport')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_sport.settings')
        
        import django
        django.setup()
        
        from django.conf import settings
        db_engine = settings.DATABASES['default']['ENGINE']
        db_name = settings.DATABASES['default'].get('NAME', 'N/A')
        
        is_postgresql = 'postgresql' in db_engine.lower()
        print(f"   数据库引擎: {db_engine}")
        print(f"   数据库名称: {db_name}")
        
        if is_postgresql:
            print("   [OK] 使用PostgreSQL数据库")
            results["database_engine"] = True
        else:
            print(f"   [X] 未使用PostgreSQL (使用: {db_engine.split('.')[-1]})")
            
    except Exception as e:
        print(f"   [X] 无法加载Django设置: {e}")
    
    # 3. 测试数据库连接
    print("\n3. 测试数据库连接:")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"   [OK] 连接成功 (测试查询结果: {result})")
            results["connection_test"] = True
            
            # 检查是否是PostgreSQL
            if hasattr(connection, 'pg_version'):
                print(f"   PostgreSQL版本: {connection.pg_version}")
                
    except Exception as e:
        print(f"   [X] 连接失败: {e}")
    
    # 4. 检查PostgreSQL服务状态
    print("\n4. 检查PostgreSQL服务状态:")
    try:
        import subprocess
        # 检查PostgreSQL服务
        result = subprocess.run(
            ['sc', 'query', 'postgresql-x64-18'],
            capture_output=True,
            text=True,
            shell=True
        )
        
        if 'RUNNING' in result.stdout:
            print("   [OK] PostgreSQL服务正在运行")
            results["postgresql_service"] = True
        else:
            print("   [!] PostgreSQL服务未运行或未找到")
            
    except Exception as e:
        print(f"   [!] 无法检查服务状态: {e}")
    
    # 5. 总结报告
    print("\n" + "=" * 60)
    print("检查结果总结:")
    print("=" * 60)
    
    # 判断是否连接到PostgreSQL
    is_connected_to_postgresql = (
        results["environment_variable"] and 
        results["database_engine"] and 
        results["connection_test"]
    )
    
    if is_connected_to_postgresql:
        print("[OK] 项目已成功连接到PostgreSQL数据库")
        print("   所有检查项通过:")
        print(f"   - 环境变量: {'[OK]' if results['environment_variable'] else '[X]'}")
        print(f"   - 数据库引擎: {'[OK]' if results['database_engine'] else '[X]'}")
        print(f"   - 连接测试: {'[OK]' if results['connection_test'] else '[X]'}")
        print(f"   - 服务状态: {'[OK]' if results['postgresql_service'] else '[!]'}")
    else:
        print("[X] 项目未连接到PostgreSQL数据库")
        print("   详细状态:")
        print(f"   - 环境变量DATABASE_URL: {'[OK] 已设置' if results['environment_variable'] else '[X] 未设置'}")
        print(f"   - 使用PostgreSQL引擎: {'[OK] 是' if results['database_engine'] else '[X] 否'}")
        print(f"   - 数据库连接: {'[OK] 成功' if results['connection_test'] else '[X] 失败'}")
        print(f"   - PostgreSQL服务: {'[OK] 运行中' if results['postgresql_service'] else '[!] 未运行/未检查'}")
        
        # 提供建议
        print("\n[提示] 切换到PostgreSQL的建议:")
        if not results["environment_variable"]:
            print("   1. 设置环境变量 DATABASE_URL")
            print("      set DATABASE_URL=postgresql://user:password@localhost:5432/dbname")
        if not results["database_engine"]:
            print("   2. 确保settings.py配置正确")
            print("      检查DATABASES配置是否使用'django.db.backends.postgresql'")
        if not results["postgresql_service"]:
            print("   3. 启动PostgreSQL服务")
            print("      net start postgresql-x64-18")
    
    return is_connected_to_postgresql

def quick_check():
    """快速检查方法"""
    print("\n快速检查方法:")
    print("-" * 40)
    
    # 方法1: 检查环境变量
    db_url = os.environ.get('DATABASE_URL')
    print(f"1. 环境变量 DATABASE_URL: {'✅ 已设置' if db_url else '❌ 未设置'}")
    
    # 方法2: 简单Python检查
    try:
        sys.path.insert(0, 'ai_sport')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_sport.settings')
        import django
        django.setup()
        from django.conf import settings
        db_engine = settings.DATABASES['default']['ENGINE']
        is_pg = 'postgresql' in db_engine.lower()
        print(f"2. 数据库引擎: {db_engine}")
        print(f"   使用PostgreSQL: {'✅ 是' if is_pg else '❌ 否'}")
    except:
        print("2. 无法检查数据库配置")
    
    # 结论
    if db_url and 'postgresql' in db_url:
        print("\n🔍 结论: 项目配置为使用PostgreSQL")
    else:
        print("\n🔍 结论: 项目可能未使用PostgreSQL")

if __name__ == "__main__":
    # 运行完整检查
    check_postgresql_connection()
    
    print("\n" + "=" * 60)
    print("提示: 运行 quick_check() 进行快速检查")
    print("=" * 60)
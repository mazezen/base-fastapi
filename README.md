# Base FastAPI Demo Project

> 这是一个演示项目，展示了具有常见功能和最佳实践的基本 FastAPI 应用程序结构

## 功能

- FastAPI：一个现代、快速（高性能）的 web 框架，用于基于标准 Python 类型提示使用 Python 3.7+构建 API。
- Uvicorn：用于运行 FastAPI 应用程序的 ASGI 服务器。
- Pydantic：用于使用 Python 类型提示进行数据验证和设置管理。
- SQLAlchemy：用于数据库 ORM（对象关系映射器）。
- JWT Authentication：使用 JSON Web 令牌进行用户身份验证。
- Dependency Injection: FastAPI 的依赖注入系统。
- Docker：容器化，便于开发和部署。
- Pytest：用于编写和运行测试。
- Coverage：用于测量代码覆盖率。
- Ruff：用于 linting 和格式化代码。
- Pre-commit：用于在提交代码之前运行检查。
- Makefile：用于常见任务的自动化。

## 环境依赖

Python 3.12+
Docker (可选，用于容器化）
Docker Compose (可选，用于容器化）

## 使用

1. 克隆

```shell
git clone https://github.com/mazezen/base-fastapi
cd base-fastapi
```

2. 创建一个虚拟环境

```shell
python3 -m venv .venv
source .venv/bin/activate
```

3. 安装依赖

```shell
python -m pip install uv (可选)
uv add poetry  || pip install poetry
poetry install
```

4. 创建 .env

```shell
cp .env.example .env
```

5. 初始化数据库

```shell
python app/db/init_db.py || make migrations message="Create initial migration"
```

6. 数据库迁移

```shell
make migrate
```

7. 运行项目

```shell
make run || uvicorn app.main:app --reload
```

8. Pycharm Debug

```text
1. Edit Configuration -> Python -> script ($(pwd)/.venv/bin/uvicorn) -> Parameters (app.main:app --host 0.0.0.0 --port 9000 --reload)
```

9. 访问 API 文档

```text
http://127.0.0.1:8000/docs (Swagger UI)
http://127.0.0.1:8000/redoc (ReDoc)
```

## 运行单测

```shell
make test
```

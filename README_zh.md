# ReviveIt
![Vite](https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E) ![Django REST](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white) ![PNPM](https://img.shields.io/badge/pnpm-yellow?style=for-the-badge&logo=pnpm&logoColor=white)

[![HitCount](https://img.shields.io/endpoint?logo=github&url=https%3A%2F%2Fhits.dwyl.com%2FuntrueFire%2FReviveIt.json%3Fcolor%3Dmarine)](http://hits.dwyl.com/untrueFire/ReviveIt) [![Coveralls](https://img.shields.io/coverallsCoverage/github/untrueFire/ReviveIt)](https://coveralls.io/r/untrueFire/ReviveIt) ![GitHub Release](https://img.shields.io/github/v/release/untrueFire/ReviveIt?include_prereleases&display_name=tag&style=flat)

[English](./README.md) | 中文

> 大学生经常有些物品觉得扔掉可惜，不处理又觉得浪费自己的地方。这是一个物品“复活”软件

该程序允许添加物品的信息（物品名称，物品描述，联系人信息），删除物品的信息，显示物品列表，也允许查找物品的信息

## 特性
- 实现了物品“复活”机制
- 实现了物品“复活”的一般等价物流通机制
- 实现了物品“复活”的一般等价物产生机制

## 使用方法
（推荐）首先修改 `backend/.env`，配置管理员账户和服务器密钥
```sh
docker compose up -d
```
然后在浏览器访问`http://localhost/`

# 文档
- 如果你不想配置 `PostgreSQL` 环境，取消 `backend/reviveit_backend/settings.py` 中 `102-105` 的注释来将数据库切换到 `sqlite3` 
- 直接使用 `docker run --rm -d -p80:80 --env-file ./backend/.env reviveit-backend` 单独启动后端（你可能首先需要使用 `sqlite3` 作为数据库构建镜像）
- 然后可以在`http://localhost/`（交互式 `Swagger Ui` 格式） 或 `http://localhost/redoc`（`ReDoc` 格式）查看API文档

## 设计文档（检查要求）
- 见 [文档](./docs/readme.md)

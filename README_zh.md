# ReviveIt
[![HitCount](https://img.shields.io/endpoint?url=https%3A%2F%2Fhits.dwyl.com%2FuntrueFire%2FReviveIt.json%3Fcolor%3Dmarine)](http://hits.dwyl.com/untrueFire/ReviveIt) [![Coverage](https://coveralls.io/repos/github/untrueFire/ReviveIt/badge.svg)](https://coveralls.io/r/untrueFire/ReviveIt) [![Django CI](https://github.com/untrueFire/ReviveIt/actions/workflows/django.yml/badge.svg)](https://github.com/untrueFire/ReviveIt/actions/workflows/django.yml)

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
- API文档可以在`http://localhost:8000/`（交互式 `Swagger Ui` 格式） 或 `http://127.0.0.1:8000/redoc`（`ReDoc` 格式）查看

## 提示
开发中，随时可能有破坏性变更

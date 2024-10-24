# ReviveIt
[![HitCount](https://img.shields.io/endpoint?url=https%3A%2F%2Fhits.dwyl.com%2FuntrueFire%2FReviveIt.json%3Fcolor%3Dmarine)](http://hits.dwyl.com/untrueFire/ReviveIt) [![Coverage](https://coveralls.io/repos/github/untrueFire/ReviveIt/badge.svg)](https://coveralls.io/r/untrueFire/ReviveIt) [![Django CI](https://github.com/untrueFire/ReviveIt/actions/workflows/django.yml/badge.svg)](https://github.com/untrueFire/ReviveIt/actions/workflows/django.yml)

English | [中文](./README_zh.md)

> We often feel that some items are a pity to throw away, and do not deal with them and feel that they are wasting their place. This is an item "revive" software
The program allows to add item information (item name, item description, contact information), delete item information, display item list, and also allows to find item information

## Feature
- Implemented item "revival" mechanism
- Implemented the universal equivalent circulation mechanism for items "revival"
- Implemented the universal equivalent generation mechanism for item "revival"

## Usage
(Recommended) First modify `backend/.env` to configure admin account and server secret key
```sh
docker compose up -d
```
Then visit it in browser by `http://localhost/`

## Documentation
- Documentation for API can be viewed at `http://localhost:8000/`(interactive `Swagger Ui` format) or `http://127.0.0.1:8000/redoc`(`ReDoc` format)

## Notice
Always under development

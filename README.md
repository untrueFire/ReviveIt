# ReviveIt
![Vite](https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E) ![Django REST](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white) ![PNPM](https://img.shields.io/badge/pnpm-yellow?style=for-the-badge&logo=pnpm&logoColor=white)

[![HitCount](https://img.shields.io/endpoint?logo=github&url=https%3A%2F%2Fhits.dwyl.com%2FuntrueFire%2FReviveIt.json%3Fcolor%3Dmarine)](http://hits.dwyl.com/untrueFire/ReviveIt) [![Coveralls](https://img.shields.io/coverallsCoverage/github/untrueFire/ReviveIt)](https://coveralls.io/r/untrueFire/ReviveIt) ![GitHub Release](https://img.shields.io/github/v/release/untrueFire/ReviveIt?include_prereleases&display_name=tag&style=flat)

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
- Directly start the backend separately by `docker run --rm -d -p80:80 --env-file ./backend/.env reviveit-backend`
- Documentation for API can then be viewed at `http://localhost/`(interactive `Swagger Ui` format) or `http://localhost/redoc`(`ReDoc` format)

## Notice
Always under development

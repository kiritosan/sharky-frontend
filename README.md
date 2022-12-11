# Sharky人群计数系统

## 项目介绍

Sharky人群计数系统前端界面，基于streamlit开发。

Sharky人群计数系统后端API，基于fastapi开发。

Sharky人群技术系统后端API，基于flask以及pytorch开发。

Sharky人群基数系统机器人，基于nonebot2以及go-cqhttp开发。

## 项目运行

具体见总项目的README.md

## 项目结构

```text
📦frontend
 ┣ 📂.vscode
 ┃ ┣ 📜launch.json
 ┃ ┗ 📜settings.json
 ┣ 📂src
 ┃ ┣ 📂assets
 ┃ ┃ ┣ 📜error.png
 ┃ ┃ ┣ 📜favicon.png
 ┃ ┃ ┣ 📜favicon.svg
 ┃ ┃ ┣ 📜logo.png
 ┃ ┃ ┣ 📜logo.svg
 ┃ ┃ ┗ 📜placeholder.png
 ┃ ┣ 📜basic_config.py
 ┃ ┣ 📜main.py
 ┃ ┣ 📜render.py
 ┃ ┣ 📜utils.py
 ┃ ┗ 📜__init__.py
 ┣ 📜.dockerignore
 ┣ 📜.git
 ┣ 📜.gitignore
 ┣ 📜Dockerfile
 ┣ 📜poetry.lock
 ┣ 📜pyproject.toml
 ┣ 📜README.md
 ┗ 📜requirements.txt

📦backend
 ┣ 📂.vscode
 ┃ ┣ 📜launch.json
 ┃ ┗ 📜settings.json
 ┣ 📂doc
 ┣ 📂src
 ┃ ┣ 📂app
 ┃ ┃ ┣ 📜main.py
 ┃ ┃ ┣ 📜utils.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂oss
 ┃ ┃ ┣ 📜oss_init.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂routers
 ┃ ┃ ┣ 📜bots.py
 ┃ ┃ ┣ 📜histories.py
 ┃ ┃ ┣ 📜images.py
 ┃ ┃ ┣ 📜videos.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┗ 📂sql
 ┃   ┣ 📜crud.py
 ┃   ┣ 📜database.py
 ┃   ┣ 📜db_init.py
 ┃   ┣ 📜models.py
 ┃   ┣ 📜schemas.py
 ┃   ┣ 📜sharky.session.sql
 ┃   ┗ 📜__init__.py
 ┣ 📂static
 ┃ ┣ 📜attack_bell.mp3
 ┃ ┣ 📜calling.mp3
 ┃ ┣ 📜siren2.mp3
 ┃ ┣ 📜strange_bell.mp3
 ┃ ┗ 📜water_land.mp3
 ┣ 📜.dockerignore
 ┣ 📜.git
 ┣ 📜.gitignore
 ┣ 📜Dockerfile
 ┣ 📜poetry.lock
 ┣ 📜pyproject.toml
 ┣ 📜README.md
 ┗ 📜requirements.txt

📦engine
 ┣ 📂.vscode
 ┃ ┣ 📜launch.json
 ┃ ┗ 📜settings.json
 ┣ 📂crowd_datasets
 ┃ ┣ 📂SHHA
 ┃ ┃ ┣ 📜loading_data.py
 ┃ ┃ ┣ 📜SHHA.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┗ 📜__init__.py
 ┣ 📂models
 ┃ ┣ 📜backbone.py
 ┃ ┣ 📜matcher.py
 ┃ ┣ 📜p2pnet.py
 ┃ ┣ 📜vgg_.py
 ┃ ┗ 📜__init__.py
 ┣ 📂pth
 ┃ ┗ 📂checkpoints
 ┃   ┣ 📜vgg16-397923af.pth
 ┃   ┗ 📜vgg16_bn-6c64b313.pth
 ┣ 📂util
 ┃ ┣ 📜misc.py
 ┃ ┗ 📜__init__.py
 ┣ 📂web
 ┃ ┣ 📜hash_values.py
 ┃ ┣ 📜oss_init.py
 ┃ ┗ 📜__init__.py
 ┣ 📂weights
 ┃ ┗ 📜SHTechA.pth
 ┣ 📜.dockerignore
 ┣ 📜.git
 ┣ 📜.gitignore
 ┣ 📜app.py
 ┣ 📜docker-compose.yml
 ┣ 📜Dockerfile
 ┣ 📜engine.py
 ┣ 📜gunicorn_config.py
 ┣ 📜LICENSE
 ┣ 📜oss_init.py
 ┣ 📜poetry.lock
 ┣ 📜pyproject.toml
 ┣ 📜README.md
 ┣ 📜requirements.txt
 ┣ 📜run_test.py
 ┣ 📜train.py
 ┗ 📜utils.py
```

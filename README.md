# auth_service

## Установка и запуск
1) Клонировать репозиторий 
```sh
git clone https://github.com/AlexanderZah/auth_service.git
```
2) Создать виртуальное окружение
```sh
python -m venv venv
```

3) Активировать виртуальное окружение
```sh
./venv/Scripts/activate.ps1
```

4) Установить зависимости
```sh
pip install -r requirements.txt
```

5) Запустить сервер 
```sh
uvicorn server:app --reload
```

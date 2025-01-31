@echo off
chcp 65001

echo Проверка наличия Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python не установлен.
    start https://www.python.org/downloads/
    pause
    exit /b
)

echo Проверка наличия pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip не установлен.
    python -m ensurepip --default-pip
)

echo Проверка наличия виртуальной среды...
if not exist ".venv" (
    echo Создание виртуальной среды...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo Не удалось создать виртуальную среду.
        pause
        exit /b
    )
)

echo Активация виртуальной среды...
call .venv\Scripts\activate

echo Установка зависимостей из requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Не удалось установить зависимости. Проверьте requirements.txt.
    pause
    exit /b
)

echo Запуск PyInstaller для создания .exe файла...
pyinstaller --onefile --add-data "share\eff_large.wordlist;share" main.py
if %errorlevel% neq 0 (
    echo Ошибка при создании .exe файла с помощью PyInstaller.
    pause
    exit /b
)

echo Создание .exe файла завершено.
pause

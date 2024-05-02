# Импорт недавно установленного пакета setuptools.
# Upload package to PyPi.
# pip install -e . # install from setup.py
# first variant build  -> python setup.py sdist bdist_wheel
# second variant build -> python -m build
# python -m twine upload --repository testpypi dist/*
# python -m twine upload --repository pypi dist/*
# python -m twine upload --repository pypi dist/w-render-0.2.3.tar.gz
# https://setuptools.pypa.io/en/latest/userguide/entry_point.html
from setuptools import setup, find_packages

# Открытие README.md и присвоение его long_description.
with open("README.md", "r") as fh:
    long_description = fh.read()

# Функция, которая принимает несколько аргументов. Она присваивает эти значения пакету.
setup(
    # Имя дистрибутива пакета. Оно должно быть уникальным, поэтому добавление вашего имени пользователя в конце является обычным делом.
    name="w-render",
    # Номер версии вашего пакета. Обычно используется семантическое управление версиями.
    version="0.3.1",
    # Имя автора.
    author="Andrey Plugin",
    # Его почта.
    author_email="9keepa@gmail.com",
    # Краткое описание, которое будет показано на странице PyPi.
    description="Render a dynamical sites.",
    # Длинное описание, которое будет отображаться на странице PyPi. Использует README.md репозитория для заполнения.
    long_description=long_description,
    # Определяет тип контента, используемый в long_description.
    long_description_content_type="text/markdown",
    # URL-адрес, представляющий домашнюю страницу проекта. Большинство проектов ссылаются на репозиторий.
    # Находит все пакеты внутри проекта и объединяет их в дистрибутив.
    packages=[
        "web_render",
        "web_render.base",
    ],
    entry_points={
        'console_scripts': []
    },
    # requirements или dependencies, которые будут установлены вместе с пакетом, когда пользователь установит его через pip.
    install_requires=[
        "selenium",
        "webdriver-manager",
        "undetected-chromedriver",
        "python-dotenv"
    ],
    # Требуемая версия Python.
    python_requires='>=3.8',
    # лицензия
    license='MIT',
)
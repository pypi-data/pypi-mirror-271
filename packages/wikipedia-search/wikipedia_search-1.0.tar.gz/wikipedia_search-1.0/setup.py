from setuptools import setup, find_packages

setup(
    name='wikipedia-search',  # Имя вашего пакета
    version='1.0',  # Версия вашего пакета
    author='k0ng999',  # Ваше имя или имя вашего проекта
    author_email='baydar_14@mail.ru',  # Ваш адрес электронной почты
    description='A program for searching and reading Wikipedia articles in multiple languages',  # Краткое описание вашего пакета
    long_description=open('README.md', encoding='utf-8').read(),  # Длинное описание вашего пакета из файла README.md
    long_description_content_type='text/markdown',  # Тип длинного описания (markdown)
    packages=find_packages(),  # Список пакетов Python, которые должны быть включены в ваш пакет
    entry_points={
        'console_scripts': [
            'search-wikipedia = wikipedia_search:search_wikipedia',  # Точка входа для вашего скрипта
        ],
    },
    install_requires=[
        'wikipedia',  # Зависимости вашего пакета
        'pyttsx3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

import setuptools

setuptools.setup(
    name="verbose_name_adder_Sino0on",  # Название пакета
    version="0.0.1",  # Версия пакета
    author="Sino0on",  # Автор
    author_email="unfazedunit@gmail.com",  # Почта автора
    description="A small example package",  # Краткое описание
    long_description="README.md",  # Подробное описание
    long_description_content_type="text/markdown",  # Тип содержимого описания
    url="https://github.com/Sino0on/verbose_name_adder",  # Ссылка на проект
    packages=setuptools.find_packages(),  # Автоматический поиск пакетов в проекте
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # Классификаторы пакета
    python_requires='>=3.6',  # Требования к версии Python
)

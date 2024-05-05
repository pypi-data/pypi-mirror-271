from setuptools import setup, find_packages


# Function to read the contents of the requirements file
def read_requirements():
    with open('requirements.txt', 'r') as req:
        # Exclude any comments or empty lines
        return [line.strip() for line in req if line.strip() and not line.startswith('#')]


# Call the function and store the requirements list
install_requires = read_requirements()

setup(
    name="try_pub_pypi",  # Назва вашого пакету
    version="0.0.2",  # Початкова версія
    author="seroleksiienko",  # Ваше ім'я або ім'я організації
    author_email="seroleksiienko@gmail.com",  # Ваша електронна адреса
    description="A small example package",  # Короткий опис пакету
    long_description=open('README.md').read(),  # Довгий опис з файлу README.md
    long_description_content_type="text/markdown",  # Тип вмісту довгого опису
    url="https://github.com/seralekseenko/try_pub_pypi",  # URL вашого проекту
    packages=find_packages(),  # Автоматичне виявлення пакетів
    entry_points={
        'console_scripts': [
            'try_pub_pypi = main_packg.main:main',  # Вказання на точку входу для виконання команди з консолі
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Мінімальна версія Python
    install_requires=install_requires
)

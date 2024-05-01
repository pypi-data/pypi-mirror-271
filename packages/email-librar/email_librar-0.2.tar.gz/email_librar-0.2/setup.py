from setuptools import setup, find_packages

setup(
    name='email_librar',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'smtplib',
    ],
    author='Ваше имя',
    author_email='ваш.емейл@example.com',
    description='Простая библиотека для отправки электронных писем на Python.',
    url='https://github.com/вашеимя/email-library',
)


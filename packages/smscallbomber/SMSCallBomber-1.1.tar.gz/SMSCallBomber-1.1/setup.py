from setuptools import setup, find_packages

setup(
    name='SMSCallBomber',
    version='1.1',
    packages=find_packages(),
    author='BabayVadimovich',
    author_email='hmatvej49@gmail.com',
    description={
    'A library for SMS and call bomber / Библиотека для SMS бомбера со звонками',
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/BabayVadimovich/SMSCallBomber',
    install_requires=[
        'requests',
        'argparse',
        'urllib3'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='bomber, sms, call, smsbomber',
)
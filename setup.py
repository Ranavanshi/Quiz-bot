from setuptools import setup, find_packages

setup(
    name='Quiz-bot',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'python-telegram-bot==13.7',
        'pymongo==3.12.0',

        # Add any other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'Quiz-bot = Quiz-bot:main',  # Adjust the entry point based on your script structure
        ],
    },
    author='Divyanshu Rana',
    description='A Telegram quiz bot',
    url='https://github.com/Ranavanshi/Quiz-bot',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

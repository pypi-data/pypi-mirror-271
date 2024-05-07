from setuptools import setup, find_packages

setup(
    name='dinosaur-run-game',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pygame',
    ],
    entry_points={
        'console_scripts': [
            'dino-game = dino_game:main',  # Adjusted entry point to match the filename
        ],
    },
    author='Your Name',
    description='A simple dinosaur run game.',
    url='https://github.com/worasit/speech_recognition',
)

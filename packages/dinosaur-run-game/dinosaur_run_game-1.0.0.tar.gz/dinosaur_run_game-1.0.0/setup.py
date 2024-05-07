from setuptools import setup, find_packages

setup(
    name='dinosaur-run-game',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pygame',  # Add any dependencies your game requires
    ],
    entry_points={
        'console_scripts': [
            'dinosaur-run = dino_game.main:main',  # Adjust the entry point to match your game's structure
        ],
    },
    author='Your Name',
    description='A simple dinosaur run game.',
    url='https://github.com/worasit/speech_recognition',
)

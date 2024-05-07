from setuptools import setup, find_packages

setup(
    name='nongped-rungame',
    version='1.0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pygame',
    ],
    entry_points={
        'console_scripts': [
            'nongped-rungame = dino_game:main',  # Adjusted entry point to match the filename
        ],
    },
    author='Worasit D.',
    description='A simple dinosaur run game.',
    url='https://github.com/worasit/speech_recognition',
)

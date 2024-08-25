from setuptools import setup, find_packages

setup(
    name='meu_jogo',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pygame>=2.5.2',
    ],
    entry_points={
        'console_scripts': [
            'meu_jogo=meu_jogo.__main__:main'
        ]
    },
    author='Carlos Hernani e João Delomo',
    author_email='carloshcdpg@al.insper.edu.br'+ "joaodelomo@al.insper.edu.br",
    description='Um jogo divertido feito com Pygame.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/JoaoDelomo/pygame_alglin',  # Substitua pelo link do seu repositório
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)

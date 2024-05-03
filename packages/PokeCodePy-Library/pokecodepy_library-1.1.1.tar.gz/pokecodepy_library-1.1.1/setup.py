from setuptools import setup, find_packages

setup(
    name='PokeCodePy_Library',
    version='1.1.1',
    author='Luz Lizeth Vazquez Garcia',
    author_email='luzlizet35@gmail.com',
    description='Biblioteca que con la clase RandomPokemon para generar un pokemon aleatorio',
    packages=["PokeCodePy_Library"],
    package_data={'PokeCodePy_Library': ['pokemon.csv']},
    install_requires=[
        'pandas',
        'twine',
        'wheel',
        'setuptools',
    ],
)

from setuptools import setup

setup(
    name='Pokemon_t2_tap',
    version='1.1.0',
    author='Uriel Franco',
    author_email='<202227011_FRANCO@tesch.edu.mx>',
    description='Una biblioteca que contiene la clase RandomPokemon para generar un Pokemon aleatorio',
    packages=["Pokemon-t2-tap"],
    package_data={'Pokemon-t2-tap': ['pokemon.csv']},
    install_requires=[
        'pandas',
    ],
)

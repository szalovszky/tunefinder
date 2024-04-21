from setuptools import setup, find_packages

setup(
    name='tunefinder',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'deezer-python~=6.1.1',
        'spotipy~=2.23.0',
        'jsonpickle~=3.0.3',
        'asyncio~=3.4.3',
        'shazamio~=0.5.1'
    ],
    entry_points={
        'console_scripts': [
            'tunefinder=tunefinder.__init__:__main__',
        ],
    },
    author='Szalovszky Dávid',
    author_email='david@szalovszky.com',
    description='A hassle-free, lightweight solution for seamlessly finding songs between streaming platforms.',
    url='https://github.com/szalovszky/tunefinder',
    license='MIT',
    python_requires='>=3.10',
)

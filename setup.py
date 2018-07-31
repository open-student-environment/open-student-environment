from setuptools import setup

setup(
    name='ose',
    description=('Playground for training and experimenting student models '
                 'using xAPI data.'),
    version='0.0',
    authors=['Arnaud Rachez', 'David Panou'],
    author_email=['arnaud.rachez@gmail.com', 'david.panou@gmail.com'],
    packages=['ose'],
    requires=['numpy', 'scipy', 'pymc'],
)

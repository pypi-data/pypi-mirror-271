from setuptools import setup, find_packages

setup(
    name='nirvana_ui',
    version='1.0',
    description='A Django app containing a UI library for easy integration into Django projects.',
    author='Kris Patel',
    author_email='krishp759@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=2.0',
    ],
)

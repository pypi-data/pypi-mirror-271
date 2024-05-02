from setuptools import setup, find_packages


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()


setup(
    name="tassosgeomath",
    version="2.0.0",
    packages=find_packages(include=['tassosgeomath', 'tassosgeomath.*']),
    install_require=[],
    url='',
    LICENCE="MIT",
    author="Tasso",
    description="This is my geometry calculator package",
    long_description=read_file(file_name="README.md"),
    python_requires=">3.6"
)

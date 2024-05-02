from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md","r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hack4u_luis",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    author="Luis Ramos",
    description="Una biblioteca para consultar cursos de hack4u.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://lramosdev.com"
)

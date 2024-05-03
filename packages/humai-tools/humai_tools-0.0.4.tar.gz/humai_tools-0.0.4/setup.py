from setuptools import setup
from setuptools import find_packages


setup(
    name="humai_tools",
    version="0.0.4",
    packages=find_packages(),
    install_requires=[
        "mercadopago",
        "requests",
        "unidecode",
        "pydantic",
        "python-dotenv",
    ],
    author="Humai Dev Team",
    author_email="mg@humai.com.ar",
    description="Internal tools for private usage.",
    long_description_content_type="text/markdown",
    long_description="Internal tools for private usage.",
    url="https://github.com/institutohumai/humai_internal_tools",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
    ],
)

from setuptools import setup, find_packages
from os import path


setup(
    name="pdfplumber-aemc",
    url="https://github.com/jsvine/pdfplumber",
    author="Jeremy Singer-Vine + Liew Chun Fui",
    author_email="wargreymon28@gmail.com",
    description="Plumb a PDF for detailed information about each char, rectangle, and line.",
    version="0.11.1",
    packages=find_packages(
        exclude=[
            "test",
        ]
    ),
    include_package_data=True,
    package_data={"pdfplumber": ["py.typed"]},
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        'Pillow>=9.1',
        'pypdfium2>=4.18.0',
    ],
    entry_points={"console_scripts": ["pdfplumber = pdfplumber.cli:main"]},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

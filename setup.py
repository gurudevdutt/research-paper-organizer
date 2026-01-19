from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="research-paper-organizer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Tools for organizing research papers and generating literature review spreadsheets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/research-paper-organizer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.7",
    install_requires=[
        "PyPDF2>=3.0.0",
        "openpyxl>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "organize-papers=organize_papers:main",
            "reorganize-folders=reorganize_folders:main",
        ],
    },
)

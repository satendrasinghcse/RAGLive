from setuptools import setup, find_packages

setup(
    name="RagAgenticSystem",
    version="0.1.0",
    author="Satendra Singh",
    author_email="",
    url="https://github.com/satendrasinghcse",
    description="Rag Agentic System - A local Python package",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # adjust as needed
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

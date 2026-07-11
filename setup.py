from setuptools import setup, find_packages

setup(
    name="dsa",
    version="0.1.0",
    description="Python implementations of data structures and algorithms",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0"],
    },
)

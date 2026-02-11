"""
Setup configuration for overfitting-demo package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = (this_directory / "requirements.txt").read_text().splitlines()
requirements = [r.strip() for r in requirements if r.strip() and not r.startswith("#")]

setup(
    name="overfitting-demo",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Interactive demonstration of overfitting in algorithmic trading",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/overfitting-demo",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "pylint>=2.17.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "overfitting-demo=src.app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

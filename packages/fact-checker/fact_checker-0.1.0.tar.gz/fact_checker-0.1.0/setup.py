from setuptools import setup, find_packages

setup(
    name="fact_checker",
    version="0.1.0",
    author="Andrew Clayman",
    author_email="drewclayman@gmail.com",
    description="A fact checker with justification",
    packages=find_packages(),
    install_requires=[
        "accelerate>=0.21.0",
        "torch",
        "transformers",
        "pandas",
        "scikit-learn",
        "numpy",
        "requests",
        "imbalanced-learn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

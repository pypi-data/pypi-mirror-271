from setuptools import setup

requirements = [
    "numpy",
    "scipy",
    "scikit-learn",
    "matplotlib",
    "tqdm",
]

requirements_dev = ["black", "isort", "flake8", "pre-commit"]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="desgld",
    version="0.1.2",
    description="Package for decentralized stochastic gradient descent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrislambd/desgld_package.git",
    author="Rafiq Islam",
    packages=["desgld"],
    package_dir={"": "src"},
    install_requires=requirements,
    extras_require={"dev": requirements_dev},
)

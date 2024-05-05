from setuptools import find_packages, setup

setup(
    name="TrainingAnimation",
    version="0.0.12",
    description="Training AI model progress bar",
    long_description="lol",
    long_description_content_type="text/x-rst",
    packages=find_packages(),
    author="MaciejM",
    install_requires=["numpy >= 1.26.3"],
    python_requires=">=3.6",
)
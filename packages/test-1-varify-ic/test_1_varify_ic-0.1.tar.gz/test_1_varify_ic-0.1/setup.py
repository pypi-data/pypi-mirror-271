from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="test_1_varify_ic",
    version="0.1",
    author="ic",
    author_email="quattroporte54@gmail.com",
    description="testing and debugging project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
)

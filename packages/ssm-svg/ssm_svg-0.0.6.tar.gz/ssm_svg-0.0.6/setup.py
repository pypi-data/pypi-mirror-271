import pathlib
from setuptools import setup, find_packages

# The directory containing this file
ROOT_DIR = pathlib.Path(__file__).parent

# The text of the README file
README = (ROOT_DIR / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ssm-svg",
    version="0.0.6",
    description="SVG spritesheet maker",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/obeezzy/ssm",
    author="Chronic Coder",
    author_email="efeoghene.obebeduo@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["lxml"],
    entry_points={
        "console_scripts": ["ssm=ssm.ssm:main"]
    },
)

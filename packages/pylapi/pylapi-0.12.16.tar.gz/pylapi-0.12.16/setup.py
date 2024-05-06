import setuptools
import os

about = {}
with open(f"{os.path.abspath(os.path.dirname(__file__))}/src/pylapi/__version__.py", "r") as f:
    exec(f.read(), about)

with open("OVERVIEW.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name=about["__name__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    license=about["__license__"],

    packages=[about["__name__"]],
    package_data={"": ["LICENSE"]},
    package_dir={"": "src"},
    python_requires=">=3.7",

    install_requires=[
        "magico>=0.3.3",
        "urllib3>=1.21.1,<1.27",
        "requests>=2.5",
        "PyYAML>=5.1",
    ],

    project_urls={
        "Source": about["__url__"],
        "Documentation": about["__url__"] + "/blob/main/tutorials",
        "Bug Tracker": about["__url__"] + "/issues",
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

dev_requires = [
    "graphene-django>=2.8.0",
]

setuptools.setup(
    name="graphene-validation",
    version="0.0.1",
    author="Wojciech Nosal",
    author_email="wnosal@outlook.com",
    description="Graphene Custom Mutation with validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WojtekNosal/graphene-validation",
    packages=setuptools.find_packages(exclude=["tests", "tests.*", "examples"]),
    install_requires=["graphene>=2.1.8", "Django>=3.0.2"],
    extras_require={"dev": dev_requires},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

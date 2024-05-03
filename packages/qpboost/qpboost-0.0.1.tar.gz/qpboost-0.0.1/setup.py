import setuptools

setuptools.setup(
    name="qpboost",
    version="0.0.1",
    author="Ilker Birbil",
    author_email="sibirbil@gmail.com",
    description="A Python package for Quadratic Programming Boosting algorithms",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sibirbil/QPBoost",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify Python version requirements
)

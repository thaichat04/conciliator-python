import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="conciliator-python", # Replace with your own username
    version="0.0.1",
    author="Dhatim",
    author_email="contact@dhatim.com",
    description="Python library for the Conciliator API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dhatim/conciliator-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['requests', 'pyjwt'],
    tests_require=['python-slugify',],

)
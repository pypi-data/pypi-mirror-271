from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    version="0.1.0",
    name="gr1336_toolbox",
    description="Personal collection of reusable tools in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gr1336/gr1336_toolbox/",
    install_requires=[
        "markdownify==0.12.1",
        "markdown2>=2.4.13",
        "numpy>=1.26.4",
        "pyperclip>=1.8.2",
        "textblob>=0.18.0",
        "pyyaml>= 6.0.0",
        "pyarrow>= 16.0.0",
    ],
    author="gr1336",
    license="MIT License (MIT)",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)

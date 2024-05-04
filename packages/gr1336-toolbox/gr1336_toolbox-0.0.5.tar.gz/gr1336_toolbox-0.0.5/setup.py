from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    version="0.0.5",
    name="gr1336_toolbox",
    description="Personal collection of reusable tools in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gr1336/gr1336_toolbox/",
    install_requires=["numpy", "pyperclip", "textblob", "pyyaml", "pyarrow"],
    author="gr1336",
    license=" Apache Software License",
    classifiers=[
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
    ],
)

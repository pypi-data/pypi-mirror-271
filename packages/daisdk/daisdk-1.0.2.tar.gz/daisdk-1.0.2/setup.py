from setuptools import setup
from daisdk import __version__

# 读取 README.md 内容作为长描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="daisdk",
    version=__version__,
    author="BigQuant",
    author_email="bigquant@bigquant.com",
    description="bigquant 数据SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bigquant.com",
    project_urls={"Documentation": "https://bigquant.com/wiki/doc/sdk-gMEOV2bGYi"},
    packages=["daisdk"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.2.2",
        "pyarrow==13.0.0"
    ],
    keywords="数据SDK, dai, bigquant",
    license="MIT",
    # build_with_nuitka=True,

)

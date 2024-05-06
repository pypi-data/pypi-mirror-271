from setuptools import setup, find_packages

with open("README.md", mode="r", encoding="utf-8") as f:
    readme = f.read()

VERSION = "1.1.0"

setup(
    name="azc-sdk",
    version=VERSION[:],
    description="AZC SDK for Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="ai",
    author_email="azc@tencent.com",
    url="https://git.code.tencent.com/open_sdk/azc-sdk-python",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.7",
    keywords=["AZC", "SDK"],
    include_package_data=True,
    project_urls={
        "Source": "https://git.code.tencent.com/open_sdk/azc-sdk-python",
    },
)
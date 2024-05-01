from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    install_requires = f.readlines()

setup(
    name="app-store-scraper-mod",
    version="0.3.6",
    author="Sei",
    author_email="engineering@seiright.com",
    description="Fork of cowboy-bebug: App Store Scraper with updated dependencies.",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=install_requires,
)

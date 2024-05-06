import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aidot",
    version="0.1.0",
    author="aidotdev2024",
    description="aidot control wifi lights",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "aiohttp",
        "setuptools",
    ],
    entry_points={
        'console_scripts': [
            'douyin_image=douyin_image:main'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
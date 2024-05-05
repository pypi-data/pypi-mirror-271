from setuptools import setup, find_packages

setup(
    name="connectifyai",
    version="0.1.0",
    description="A CLI to run ConnectifyAI graphs",
    url="https://connectify-ai.vercel.app",
    author="ConnectifyAI",
    author_email="connectifyai2@gmail.com",
    classifiers=[
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only"
    ],
    install_requires=[
        'Click',
        'orjson',
        'transformers',
        'datasets',
        'requests' 
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            "connect = connectifycli.cli:main",
        ],
    },
)

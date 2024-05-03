from setuptools import setup, find_packages

setup(
    name="moneymatters",
    version="2024.05.03",
    description="A Python package that encompasses money related stuff into one package - money formatting, currency conversion etc",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # Ensure you include a README.md in your package
    author="Gopala Krishna Koduri",
    author_email="gopal@riyazapp.com",
    url="https://github.com/musicmuni/moneymatters",  # Company URL
    project_urls={  # Additional URLs
        "Source Code": "https://github.com/musicmuni/moneymatters",
        "Issue Tracker": "https://github.com/musicmuni/moneymatters/issues",
        "Connect w/ Author": "https://linkedin.com/in/gopalkoduri",
        "Riyaz - Learn to sing": "https://riyazapp.com",
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=["CurrencyConverter", "requests", "beautifulsoup4"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

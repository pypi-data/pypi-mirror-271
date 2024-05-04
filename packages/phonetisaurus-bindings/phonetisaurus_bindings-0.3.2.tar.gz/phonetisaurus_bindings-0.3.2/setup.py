#!/usr/bin/python
from setuptools import setup, find_packages

with open("../README.md") as f:
    README = f.read()

#Install phonetisaurus
setup (
    name         = "phonetisaurus-bindings",
    version      = "0.3.2",
    description  = "Phonetisaurus G2P python package (OpenFst-1.7.2)",
    long_description=README,
    long_description_content_type="text/markdown",
    url          = "https://github.com/eginhard/phonetisaurus",
    author       = "Josef Novak",
    author_email = "josef.robert.novak@gmail.com",
    maintainer   = "Enno Hermann",
    maintainer_email="enno.hermann@gmail.com",
    license      = "BSD",
    packages=find_packages(),
    package_data={"phonetisaurus": [
        "Phonetisaurus.so",
        "bin/phonetisaurus-align",
        "bin/phonetisaurus-arpa2wfst",
        "bin/phonetisaurus-g2pfst",
        "bin/phonetisaurus-g2prnn",
        "bin/rnnlm",
        "bin/estimate-ngram",
        "bin/evaluate-ngram",
        "bin/interpolate-ngram",
    ]},
    scripts = [
        "bin/phonetisaurus-apply",
        "bin/phonetisaurus-train",
    ],
    entry_points = {
        "console_scripts": [
            "phonetisaurus-align = phonetisaurus.commands:ph_align",
            "phonetisaurus-arpa2wfst = phonetisaurus.commands:ph_arpa2wfst",
            "phonetisaurus-g2pfst = phonetisaurus.commands:ph_g2pfst",
            "phonetisaurus-g2prnn = phonetisaurus.commands:ph_g2prnn",
            "rnnlm = phonetisaurus.commands:rnnlm",
            "estimate-ngram = phonetisaurus.commands:estimate_ngram",
            "evaluate-ngram = phonetisaurus.commands:evaluate_ngram",
            "interpolate-ngram = phonetisaurus.commands:interpolate_ngram",
        ]
    },
    install_requires = ["bottle"],
    zip_safe     = False,
    python_requires=">=3.6.0",
    project_urls={
        "Repository": "https://github.com/eginhard/phonetisaurus",
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)

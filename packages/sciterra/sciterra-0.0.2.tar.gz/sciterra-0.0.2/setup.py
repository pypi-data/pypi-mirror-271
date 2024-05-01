import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    "ads",
    "bibtexparser",
    "gensim", # N.B.: requires scipy <= 1.10.1
    "numpy",
    "pandas",
    "plotnine",
    "scikit-learn",
    "scipy==1.10.1",
    "sentence-transformers",
    "semanticscholar==0.5.0",  # 0.6.0 has AsyncSemanticScholar which creates difficulties
    "spacy",
    "torch",
    "transformers",
]

test_requirements = [
    "black",
    "coverage",
    "pytest",
]

setuptools.setup(
    name="sciterra",
    version="0.0.2",
    author="Nathaniel Imel",
    author_email="nimel@uci.edu",
    description="Scientific literature data exploration analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nathimel/sciterra",
    project_urls={"Bug Tracker": "https://github.com/nathimel/sciterra/issues"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=requirements,
    extra_requires={"test": test_requirements},
    #    python_requires=">=3.10.6",  # Colab-compatible
    #    python_requires=">=3.9.1",  # cc-compatible
)

from setuptools import setup, find_packages

setup(
    name="NeoMind",  # Replace with your package name
    version="0.1.0",
    author="Siddartha Galipelli",
    author_email="respectsiddartha@example.com",
    description="Create your own custom AI chatbot package using Groq and Neo4j for knowledge-based responses.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Siddartha25/NeoAgent",  # Replace with your GitHub repo
    packages=find_packages(),
    install_requires=[
        "spacy",
        "neo4j",
        "numpy",
        "scikit-learn",
        "groq"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)

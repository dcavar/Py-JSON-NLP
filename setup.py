
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyjsonnlp",
    version='0.2.20',
    python_requires='>=3.6',
    author="Damir Cavar, Oren Baldinger, Maanvitha Gongalla, Anurag Kumar, Murali Kammili",
    author_email="damir@cavar.me",
    description="The Python JSON-NLP package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dcavar/Py-JSON-NLP",
    packages=setuptools.find_packages(),
    install_requires=[
        'conllu>=1.2.3',
        'jsonschemanlplab>=3.0.1.1',
        'flask',
        'iso639',
        'bs4',
        'syntok>=1.1.1',
        'aioify>=0.3.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    data_files=[('pyjsonnlp', ['pyjsonnlp/NLP-JSON.schema.json'])],
    setup_requires=["pytest-runner"],
    test_suite="tests",
    tests_require=["pytest", "coverage"]
)

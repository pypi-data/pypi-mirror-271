from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="apollo-ai",
    version="0.0.44",
    description="Framework to process 3 channels in one: Video, Audio & Text",
    package_dir={"": "apollo"},
    packages=find_packages(where="apollo"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VerbaNexAI/APOLLO.AI",
    author="VerbaNex, Riddle",
    license="GPL-3.0",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "ctranslate2==3.20.0",
        "epitran==1.24",
        "faster-whisper==0.9.0",
        "ffmpeg-python==0.2.0",
        "huggingface-hub==0.17.3",
        "Jinja2==3.1.2",
        "jiwer==3.0.3",
        "keyboard==0.13.5",
        "librosa==0.10.1",
        "llvmlite==0.41.1",
        "matplotlib==3.7",
        "mediapipe==0.10.7",
        "nltk==3.8.1",
        "numpy==1.26.1",
        "opencv-contrib-python==4.8.1.78",
        "opencv-python==4.8.1.78",
        "pandas==2.1.2",
        "Pillow==10.1.0",
        "pyphen==0.14.0",
        "scikit-learn==1.3.2",
        "scipy==1.11.3",
        "sounddevice==0.4.6",
        "soundfile==0.12.1",
        "spacy==3.7.2",
        "spacy-legacy==3.0.12",
        "spacy-loggers==1.0.5",
        "sympy==1.12",
        "tqdm==4.66.1",
        "transformers==4.34.1",
        "sixdrepnet~=0.1.6",
        "setuptools~=65.5.1",
        "moviepy~=1.0.3"
    ],
    extras_require={
        "dev": ["pytest>=7.4.3", "twine>=4.0.2"]
    },
    python_requires=">=3.10"
)

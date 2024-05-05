from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='gemini_match_word_puzzle',
    version='1',
    packages=['gemini_match_word_puzzle'],
    url='https://github.com/SoftwareApkDev/gemini_match_word_puzzle',
    license='MIT',
    author='SoftwareApkDev',
    author_email='softwareapkdev2022@gmail.com',
    description='This package contains implementation of a puzzle game on command-line interface with Google Gemini AI '
                'integrated into it.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=['gemini_ai_app_downloader'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    entry_points={
        "console_scripts": [
            "gemini_match_word_puzzle=gemini_match_word_puzzle.gemini_match_word_puzzle:main",
        ]
    }
)
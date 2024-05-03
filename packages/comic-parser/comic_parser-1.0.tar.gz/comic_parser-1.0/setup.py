import sys
from setuptools import setup, find_packages

if sys.version_info[:2] < (3, 8):
    sys.stderr.write(f'comic-parser requires Python 3.8 or later ({sys.version_info[:2]} detected).\n')
    sys.exit(1)

project_urls = {
    "Bug Tracker": "https://github.com/palvarezlopez/comic-parser/issues",
    "Documentation": "https://github.com/palvarezlopez/comic-parser",
    "Source Code": "https://github.com/palvarezlopez/comic-parser"
}

classifiers = [
    # Python version
    "Programming Language :: Python :: 3",
    # Operating system
    "Operating System :: OS Independent",
]

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

if __name__ == "__main__":
    setup(
        name = "comic-parser",
        version = "1.0",
        maintainer = "",
        maintainer_email = "",
        author = "Pablo Alvarez Lopez",
        author_email = "",
        description = "Python utility for build comics",
        keywords = ["comic", "pdf"],
        long_description = long_description,
        platforms = ["Linux", "Mac OSX", "Windows", "Unix"],
        packages = find_packages(exclude=["comic_parser.egg-info", ".git", ".vs"]),
        url = "",
        project_urls = project_urls,
        classifiers = classifiers,
        install_requires = ["img2pdf", "pillow"],
        python_requires = ">=3.7",
        zip_safe = False,
        entry_points = {"console_scripts": [ "comic-parser = comicParser:runParser"]}
    )
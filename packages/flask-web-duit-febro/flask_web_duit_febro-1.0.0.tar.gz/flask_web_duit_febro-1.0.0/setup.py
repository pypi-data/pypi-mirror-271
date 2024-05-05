import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "flask-web-duit-febro",
    version = "1.0.0",
    author = "Febrian",
    author_email = "febrian.aw20@gmail.com",
    description = "This is a package for Flask Website",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/AganFebro/flask-web",
    project_urls = {
        "Bug Tracker": "https://github.com/AganFebro/flask-web/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)

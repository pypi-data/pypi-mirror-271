from setuptools import setup, find_packages


def package_files(directory, ext=None):
    paths = []
    for path, directories, filenames in os.walk(directory):
        for filename in filenames:
            if not ext or (ext and filename.endswith(ext)):
                paths.append(os.path.join("..", path, filename))
    return paths


extra_files = [
    "../requirements.txt",
    "../requirements_basic.txt",
    "../requirements_server.txt",
    "../requirements_data.txt",
    "../requirements_interface.txt",
]

with open("requirements_basic.txt") as f:
    tmp_basic = f.read().strip().split("\n")
with open("requirements_server.txt") as f:
    tmp_server = f.read().strip().split("\n")
with open("requirements_data.txt") as f:
    tmp_data = f.read().strip().split("\n")
with open("requirements_interface.txt") as f:
    tmp_interface = f.read().strip().split("\n")

install_requires = [pos for pos in tmp_basic if pos]

extras_require = {
    "server": [pos for pos in tmp_server if pos],
    "data": [pos for pos in tmp_data if pos],
    "interface": [pos for pos in tmp_interface if pos],
}

extras_require["all"] = (
    extras_require["server"] + extras_require["data"] + extras_require["interface"]
)

setup(
    name="pytigon-batteries",
    version="0.240505",
    description="Pytigon library",
    author="Sławomir Chołaj",
    author_email="slawomir.cholaj@gmail.com",
    license="LGPLv3",
    packages=find_packages(),
    package_data={"": extra_files},
    install_requires=install_requires,
    extras_require=extras_require,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3",
)

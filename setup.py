import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nyc_intersection_geocoder",
    version="0.0.4",
    author="Wayne Lam",
    author_email="w.p.lam107@gmail.com",
    description="Package to help geocode NYC intersections with OSMPythonTools.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wplam107/nyc_intersection_geocoder",
    project_urls={
        "Bug Tracker": "https://github.com/wplam107/nyc_intersection_geocoder/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'OSMPythonTools',
        'shapely'
    ]
)
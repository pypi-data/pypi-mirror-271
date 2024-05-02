from setuptools import setup

setup(
    name="camera-ui-python-types",
    version="0.1.27",
    description="camera.ui python types",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seydx/camera.ui",
    author="seydx",
    author_email="dev@seydx.com",
    maintainer="seydx",
    maintainer_email="dev@seydx.com",
    packages=["camera_ui_python_types"],
    license="MIT",
    python_requires=">=3.8",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "rx>=3.2.0",
    ],
)

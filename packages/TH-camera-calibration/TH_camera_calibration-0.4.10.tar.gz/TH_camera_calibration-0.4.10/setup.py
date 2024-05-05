from setuptools import setup, find_packages

encodings_to_try = ["utf-8", "utf-16", "ascii", "iso-8859-1"]

for encoding in encodings_to_try:
    try:
        with open("README.md", "r", encoding=encoding) as f:
            description = f.read()
        print("Successfully read using encoding:", encoding)
        break
    except UnicodeError:
        print("Failed to read using encoding:", encoding)

setup(
    name="TH_camera_calibration",
    version="0.4.10",
    packages=find_packages(),
    install_requires=[
        "numpy==1.26.4",
        "opencv_contrib_python==4.8.1.78",
        "opencv_python==4.9.0.80",
        "PyYAML==6.0.1",
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)

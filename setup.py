from setuptools import setup, find_packages

setup(
    name="hikvision_alert",
    version="1.0.0",
    description="Procesador de eventos para cámaras Hikvision con análisis de imágenes.",
    author="Felipe Godoy",
    packages=find_packages(where="hikvision_alert"),
    package_dir={"": "hikvision_alert"},
    install_requires=[
        "requests",
        "python-dotenv",
        "PyYAML",
        "pytz",
        "opencv-python",
        "numpy",
        "urllib3"
    ],
    include_package_data=True,
    package_data={
        "hikvision_alert": [
            "yolo/*.cfg",
            "yolo/*.weights",
            "yolo/*.names"
        ]
    },
    python_requires=">=3.7",
)
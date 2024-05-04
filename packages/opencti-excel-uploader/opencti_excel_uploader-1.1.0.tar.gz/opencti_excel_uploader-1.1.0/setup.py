from setuptools import setup, find_packages

setup(
    name="opencti-excel-uploader",
    version="1.1.0",
    packages=find_packages(),
    description="Creates workbench files from excel files for Opencti",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    install_requires=[
        "pycti>=6.0.9,<7.0.0",
        "pandas>=2.2.2,<3.0.0",
        "openpyxl>=3.1.2,<4.0.0",
        "python-dotenv>=1.0.1,<2.0.0",
        "urllib3>=2.2.1,<3.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "opencti-excel-uploader=opencti_excel_uploader.__main__:main"
        ]
    },
)

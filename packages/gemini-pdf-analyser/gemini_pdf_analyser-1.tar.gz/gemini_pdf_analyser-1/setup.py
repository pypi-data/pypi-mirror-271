from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='gemini_pdf_analyser',
    version='1',
    packages=['gemini_pdf_analyser'],
    url='https://github.com/SoftwareApkDev/gemini_pdf_analyser',
    license='MIT',
    author='SoftwareApkDev',
    author_email='softwareapkdev2022@gmail.com',
    description='This package contains implementation of a PDF file analyser with Google Gemini AI '
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
            "gemini_pdf_analyser=gemini_pdf_analyser.gemini_pdf_analyser:main",
        ]
    }
)
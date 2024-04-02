from setuptools import setup, find_packages

setup(
    name='vlite',
    version='1.1.1',
    author='Surya Dantuluri',
    author_email='surya@suryad.com',
    description='A simple vector database that stores vectors in a numpy array.',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'Requests',
        'setuptools',
        'torch',
        'transformers',
        'uuid',
        'usearch',
        'PyPDF2',
        'docx2txt',
        'surya-ocr'
    ],
    # extras_require={
    #     'ocr': ['surya-ocr']
    # },
)

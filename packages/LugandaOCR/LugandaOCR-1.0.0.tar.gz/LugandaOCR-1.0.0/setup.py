from setuptools import setup, find_packages

setup(
    name='LugandaOCR',
    version='1.0.0',
    author='Beijuka',
    author_email='lugandaocr@gmail.com',
    maintainer='Beijukabruno',
    maintainer_email='lugandaocr@gmail.com',
    description='Optical Character Recognition (OCR) for Luganda language text images using TensorFlow',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'tensorflow>=2.14.0',
        'numpy',
        'pandas',
        'tqdm',
    ],
    keywords='OCR Luganda TensorFlow machine-learning',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)


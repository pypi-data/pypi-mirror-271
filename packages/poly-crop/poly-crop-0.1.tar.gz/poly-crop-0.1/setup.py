from setuptools import setup, find_packages

setup(
    name='poly-crop',
    version='0.1',
    packages=find_packages(),
    author='Your Name',
    description='Python library for cropping polygons in images',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    install_requires=[
        'numpy',
        'opencv-python',
        'Pillow',
    ],
)

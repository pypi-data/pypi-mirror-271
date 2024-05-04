from setuptools import setup, find_packages

setup(
    name='poly_crop',
    version='0.3',
    packages=find_packages(),
    author='Elias Jensen',
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

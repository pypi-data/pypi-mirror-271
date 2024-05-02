from setuptools import setup, find_packages

setup(
    name='vrt-python',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'numpy==1.26.4',
        'Pillow==10.2.0'
    ],
    entry_points={
        'console_scripts': [
            'image_diff=image_diff.image_difference:main'
        ],
    },
    author='Vladimir Shkodin',
    author_email='v.s.shkodin@gmail.com',
    description='A utility to compare images and screenshots',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/vshkodin/python-vrt',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
)


from setuptools import setup, find_packages
try:
    from install_preserve import preserve
except ImportError:
    import pip  # noqa
    pip.main(['install', 'install-preserve'])
    from install_preserve import preserve  # noqa

install_requires = [
    'numpy',
    'opencv-python',
]

exclusions = [
    'opencv-python:cv2'
]

install_requires = preserve(install_requires, exclusions, verbose=True)


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='featurecrop',
    version='0.0.1',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
        ],
    },
    author='Manbehindthemadness',
    author_email='manbehindthemadness@gmail.com',
    description='FeatureCrop is a Python library designed to automatically crop an image',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/manbehindthemadness/featurecrop',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)

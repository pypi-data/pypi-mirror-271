from setuptools import setup, find_packages

setup(
    name='opmentis',
    version='0.1.0',
    author='opmentis',
    author_email='opmentisai@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',  # Ensure you include all necessary dependencies
    ],
    python_requires='>=3.6',
    description='Library to register opmentis miners.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/OpMentis-Ai',  # Replace with the URL to your project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
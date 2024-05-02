from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
  
setup(
    name="YoutubeUser",
    version='1.2.2',
    author='R1TGAMING',
    author_email='rafisofyangaming1234@gmail.com',
    description='A Lib For Search Youtube User Or Channels',
    long_description=long_description,
    long_description_content_type='text/markdown',
   url='https://github.com/R1TGAMING/YoutubeUser',
    packages=["youtubeuser"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires= ["requests>=2.31.0"]
)

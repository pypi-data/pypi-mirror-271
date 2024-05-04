from setuptools import setup, find_packages
import pathlib


long_description = (pathlib.Path(__file__).parent / "sciborg" / "Readme.md").read_text()


setup(
    name='sciborg',
    version='0.0.1',
    author='Hedwin BONNAVAUD',
    author_email='hbonnavaud@gmail.com',
    description='Reinforcement learning library for building complex agents with simple components.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/hbonnavaud/sciborg",
    packages=find_packages(),
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=["torch", "numpy", "gym", "scikit-image", "opencv-python", "pillow", "matplotlib"]
)

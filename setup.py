from setuptools import setup, find_packages

setup(
    name='ptcq',
    version='0.1.1',
    description='PyTorch Complex Quantization',
    author='Teddy van Jerry (Wuqiong Zhao)',
    author_email='me@teddy-van-jerry.org',
    url='https://github.com/Teddy-van-Jerry/ptcq',
    packages=find_packages(),
    install_requires=[
        'torch>=1.0.0',
        'numpy>=1.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)

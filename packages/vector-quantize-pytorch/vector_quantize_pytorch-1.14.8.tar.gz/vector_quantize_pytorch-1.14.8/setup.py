from setuptools import setup, find_packages

setup(
  name = 'vector_quantize_pytorch',
  packages = find_packages(),
  version = '1.14.8',
  license='MIT',
  description = 'Vector Quantization - Pytorch',
  long_description_content_type = 'text/markdown',
  author = 'Phil Wang',
  author_email = 'lucidrains@gmail.com',
  url = 'https://github.com/lucidrains/vector-quantizer-pytorch',
  keywords = [
    'artificial intelligence',
    'deep learning',
    'pytorch',
    'quantization'
  ],
  install_requires = [
    'einops>=0.8.0',
    'einx[torch]>=0.2',
    'torch'
  ],
  extras_require = dict(
    test = [
      'torchvision',
      'tqdm'
    ]
  ),
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)

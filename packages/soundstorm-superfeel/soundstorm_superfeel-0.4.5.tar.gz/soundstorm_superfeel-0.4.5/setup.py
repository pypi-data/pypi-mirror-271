from setuptools import setup, find_packages

setup(
  name = 'soundstorm-superfeel',
  packages = find_packages(exclude=[]),
  version = '0.4.5',
  license='MIT',
  description = 'SoundStorm - Efficient Parallel Audio Generation from Google Deepmind, in Pytorch',
  author = 'Phil Wang & Oseh Mathias',
  author_email = 'o@matmail.me',
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/osehmathias/soundstorm-superfeel',
  keywords = [
    'artificial intelligence',
    'deep learning',
    'transformers',
    'attention mechanism',
    'audio generation'
  ],
  install_requires=[
    'accelerate',
    'audiolm-superfeel>=1.2.8',
    'beartype',
    'classifier-free-guidance-pytorch>=0.1.5',
    'gateloop-transformer>=0.1.1',
    'einops>=0.6.1',
    'spear-tts-pytorch>=0.4.0',
    'torch>=1.6',
  ],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)

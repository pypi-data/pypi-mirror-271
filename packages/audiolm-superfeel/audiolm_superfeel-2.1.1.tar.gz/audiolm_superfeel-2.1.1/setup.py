from setuptools import setup, find_packages
exec(open('audiolm_superfeel/version.py').read())

setup(
  name = 'audiolm-superfeel',
  packages = find_packages(exclude=[]),
  version = __version__,
  license='MIT',
  description = 'AudioLM - Language Modeling Approach to Audio Generation from Google Research - Pytorch',
  author = 'Phil Wang & Oseh Mathias',
  author_email = 'o@matmail.me',
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/osehmathias/audiolm-superfeel',
  keywords = [
    'artificial intelligence',
    'deep learning',
    'transformers',
    'attention mechanism',
    'audio generation'
  ],
  install_requires=[
    'accelerate>=0.24.0',
    'beartype>=0.16.1',
    'einops>=0.7.0',
    'ema-pytorch>=0.2.2',
    'encodec',
    'fairseq',
    'wandb',
    'gateloop-transformer>=0.2.3',
    'joblib',
    'local-attention>=1.9.0',
    'pytorch-warmup',
    'scikit-learn',
    'sentencepiece',
    'torch>=2.1',
    'torchaudio',
    'transformers',
    'tqdm',
    'vector-quantize-pytorch>=1.12.5'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)

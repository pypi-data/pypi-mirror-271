import setuptools

def find_version(path):
    for line in open(path):
        if line.startswith('__version__'):
            return line.split("=")[1].strip().replace("'", "").replace('"', '')
    else:
        raise RuntimeError("Unable to find version string.")

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='PLAID-X',
    version=find_version('./plaidx/__init__.py'),
    author='Eugene Yang',
    author_email='eugene.yang@jhu.edu',
    description="Efficient and Effective Passage Search via Contextualized Late Interaction over BERT and XLM-RoBERTa",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hltcoe/ColBERT-X/tree/plaid-x',
    packages=setuptools.find_packages(),
    install_requires=open('requirements.txt').read().split("\n"),
    include_package_data=True,
    python_requires='>=3.8',
)

from setuptools import setup, find_packages
setup(name='asyncAminoLab',
      version='1.1',
      url = 'https://github.com/l0v3m0n3y/AminoLab',
    download_url = 'https://github.com/l0v3m0n3y/AminoLab/archive/refs/heads/main.zip',
      description='async libary for aminoapps.com. ton wallet: UQAeAZH2DkWqsU8zLtdpx9ELkM0agCtCoi8myYkPOJ-9ObNS',
      author_email="pepsiritp@gmail.com",
      long_description = """# AminoLab
AminoLab Api For AminoApps using aminoapps.com/api

### Installing
`pip install AminoLab`""",
    long_description_content_type ='text/markdown',
      keywords = [
        'aminoapps',
        'amino-py',
        'amino',
        'amino-bot',
        'narvii',
        'api',
        'python',
        'python3',
        'python3.x',
        'botamino',
        'AminoLab'
    ],
    install_requires = [
        'aiohttp',
        'asyncio'
    ],
    setup_requires = [
        'wheel'
    ],
    packages = find_packages()
)
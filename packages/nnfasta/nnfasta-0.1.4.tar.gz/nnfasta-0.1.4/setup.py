# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nnfasta']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nnfasta',
    'version': '0.1.4',
    'description': 'Neural Net efficient Fasta',
    'long_description': "# nnfasta\n\nNeural Net efficient fasta Dataset for Training.\n\nShould be memory efficient across process boundaries.\nSo useful as input to torch/tensorflow dataloaders etc.\n\nPresents a list of fasta files as a simple `abc.Sequence`\nso you can inquire about `len(dataset)` and retrieve\n`Record`s with `dataset[i]`\n\n## Install\n\nInstall:\n\n```bash\npip install nnfasta\n```\n\nThere are **no** dependencies.\n\n## Usage\n\n```python\n\nfrom nnfasta import nnfastas \n\n\ndataset = nnfastas(['athaliana.fasta','triticum.fasta','zmays.fasta'])\n\n# display number of sequences\nprint(len(dataset))\n\n# get a particular record\nrec = dataset[20]\nprint('sequence', rec.id, rec.description, rec.seq)\n```\n",
    'author': 'arabidopsis',
    'author_email': 'ian.castleden@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)

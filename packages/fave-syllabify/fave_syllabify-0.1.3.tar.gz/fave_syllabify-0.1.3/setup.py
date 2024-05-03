# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fave_syllabify']

package_data = \
{'': ['*']}

install_requires = \
['aligned-textgrid>=0.6.6,<0.7.0']

setup_kwargs = {
    'name': 'fave-syllabify',
    'version': '0.1.3',
    'description': 'Syllabify force-aligned textgrids',
    'long_description': '# fave-syllabify\n\n\n![](https://img.shields.io/badge/Lifecycle-Maturing-lightgreen@2x.png)\n![PyPI version](https://badge.fury.io/py/fave-syllabify.svg) [![Lint and\nTest](https://github.com/Forced-Alignment-and-Vowel-Extraction/fave-syllabify/actions/workflows/lint-and-test.yml/badge.svg)](https://github.com/Forced-Alignment-and-Vowel-Extraction/fave-syllabify/actions/workflows/lint-and-test.yml)\n[![Build\nDocs](https://github.com/Forced-Alignment-and-Vowel-Extraction/fave-syllabify/actions/workflows/build_docs.yml/badge.svg)](https://forced-alignment-and-vowel-extraction.github.io/fave-syllabify/)\n[![codecov](https://codecov.io/gh/Forced-Alignment-and-Vowel-Extraction/fave-syllabify/graph/badge.svg?token=WDBJ0O9P6L)](https://codecov.io/gh/Forced-Alignment-and-Vowel-Extraction/fave-syllabify)\n[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10708119.svg)](https://doi.org/10.5281/zenodo.10708119)\n\nSyllabify a force-aligned TextGrid\n\n## Installation\n\n``` bash\npip install fave-syllabify\n```\n\n## Usage\n\nImport classes and functions\n\n``` python\nfrom aligned_textgrid import AlignedTextGrid, custom_classes\nfrom fave_syllabify import syllabify_tg\nfrom pathlib import Path\n```\n\nRead in a textgrid\n\n``` python\ntg = AlignedTextGrid(\n    textgrid_path=Path(\n        "docs",\n        "data",\n        "josef-fruehwald_speaker.TextGrid"\n    ),\n    entry_classes=custom_classes(\n        ["Word", "Phone"]\n    )\n)\n\nprint(tg)\n```\n\n    AlignedTextGrid with 1 groups named [\'group_0\'] each with [2] tiers. [[\'Word\', \'Phone\']]\n\nSyllabify the textgrid\n\n``` python\nsyllabify_tg(tg)\n\nprint(tg)\n```\n\n    AlignedTextGrid with 1 groups named [\'group_0\'] each with [4] tiers. [[\'Word\', \'Syllable\', \'SylPart\', \'Phone\']]\n\n### Exploring the syllabification\n\n``` python\nword_tier = tg.group_0.Word\nraindrops = word_tier[5]\n\nprint(raindrops.label)\n```\n\n    raindrops\n\nEach syllable is labelled with its stress.\n\n``` python\nprint([\n    syl.label \n    for syl in raindrops.contains\n])\n```\n\n    [\'syl-1\', \'syl-2\']\n\nEach syllable contains its constituent parts in a flat hierarchy\n(there’s no rhyme constituent).\n\n``` python\nsyl = raindrops.first.fol\nprint([\n    part.label\n    for part in syl.contains\n])\n```\n\n    [\'onset\', \'nucleus\', \'coda\']\n\nEach constituent contains its relevant phone.\n\n``` python\nonset = syl.onset\nprint([\n    phone.label\n    for phone in onset\n])\n```\n\n    [\'D\', \'R\']\n',
    'author': 'JoFrhwld',
    'author_email': 'JoFrhwld@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

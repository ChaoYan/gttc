# Graph-based Table Retrieval (GTR)
Code and data for our paper [Retrieving Complex Tables with Multi-Granular Graph Representation Learning](https://arxiv.org/abs/2105.01736) at SIGIR 2021.
Refactor Code for table type classfication and table structure recognition.

## Quick Links
  - [Preliminary](#preliminary)
  - [Run](#run)
  - [Citation](#citation)

## Preliminary

[Install requirements](https://docs.dgl.ai/en/0.4.x/install/):
```bash
pip install torch==1.9.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html
pip install dgl-cu111 dglgo -f https://data.dgl.ai/wheels/repo.html
pip insatll git+https://github.com/facebookresearch/fastText
pip install transformers pandas networkx tqdm sklearn
```

Download [pretrained word vectors](https://fasttext.cc/docs/en/pretrained-vectors.html):
```bash
wget https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.en.zip
unzip wiki.en.zip
# (move unziped files to models dir)
```

Install [trec_eval tool](https://github.com/usnistgov/trec_eval):
```bash
git clone https://github.com/usnistgov/trec_eval.git
cd trec_eval
make
# (move trec_eval to bin dir)
```

## Run
To run cross validation on WikiTables dataset:
```bash
python run.py --exp cross_validation --config configs/wikitables.json
```

To train & test on TTC dataset:
```bash
python run.py --exp train_test_ttc --config configs/tabletype.json
```

## Citation
If you use our code in your research, please cite our work:
```bibtex
@inproceedings{wang2021retrieving,
  title={Retrieving Complex Tables with Multi-Granular Graph Representation Learning},
  author={Wang, Fei and Sun, Kexuan and Chen, Muhao and Pujara, Jay and Szekely, Pedro},
  booktitle={Proceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval},
  pages={1472--1482},
  year={2021}
}
```

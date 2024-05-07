# DyHNet: Learning Dynamic Heterogeneous NetworkRepresentations


## Directory structure:

```
.
|   README.md
|   environment.yml
|   installation.txt
|
|--- dataset
|--- model
|--- ouput
|--- src
|   |-- config
|   |   dblp.json
|   |   imdb.json
|   datasets.py: data module for training
|   inference.py: inference agent
|   layer.py: layers in model
|   model.py: model module for training
|   predict_link.py: link prediction
|   utils.py: utils functions
```

## Installation

### Libraries

To install all neccessary libraries, please run:

```bash
conda env create -f environment.yml
```

In case, the version of Pytorch and Cuda are not compatible on your machine, please remove all related lib in the `.yml` file; then install Pytorch and Pytorch Geometric separately.


### PyTorch
Please follow Pytorch installation instruction in this [link](https://pytorch.org/get-started/locally/).


### Torch Geometric
```bash
pip install torch-scatter -f https://data.pyg.org/whl/torch-${TORCH}+${CUDA}.html
pip install torch-sparse -f https://data.pyg.org/whl/torch-${TORCH}+${CUDA}.html
pip install torch-cluster -f https://data.pyg.org/whl/torch-${TORCH}+${CUDA}.html
pip install torch-spline-conv -f https://data.pyg.org/whl/torch-${TORCH}+${CUDA}.html
pip install torch-geometric
```
where `${TORCH}` and `${CUDA}` is version of Pytorch and Cuda.


## Model Architecture

![Model architecture](/figure/framework.png)

## Experimental replication

### Dataset
Use dataset in the paper: 
Use your own dataset: You need to prepare four files with the following format:
    1. node_types.csv: format of each row `node_id (int), node_type (int), node_type_name (str)`

    E.g
    ```
    node_id,node_type,node_type_name
    0,0,author
    1,0,author
    2,0,author
    3,0,author
    4,0,author
    ```
    2. temporal_edge_list.txt: format of each row `source_node_id (int), target_node_id (int), time_id (int)`

    E.g.
    ```
    1840 1 6
    1840 2 6
    1840 3 6
    1841 4 4
    1841 5 4
    ```

    3. temporal_subgraphs.pth: format of each row `subgraph_ids, time_id, label`

    E.g.
    ```
    1883-90-105-12693-12812-13117-13235-13273-13682-14027-14158-14241-14387-14517	0	uai	
    1884-105-121-12736-12827-13072-13329-14517	0	uai	
    1909-182-183-12636-12640-12749-12776-12782-12807-13039-13040-13124-13676-14308-14410-14489-14519	0	cikm	
    1930-242-243-13072-13228-13702-14073-14089-14311-14519	0	cikm	
    1972-346-347-12578-12693-12893-13437-13473-13595-13740-14421-14523	0	colt	
    ```
    4. data.pkl: a dictionary for train/val/test dataloader
    E.g.


### Preprocess data
`python prepare_dataset/prepare_dataset.py`

### Train/Inference/Evaluate
`sh script/train.sh`

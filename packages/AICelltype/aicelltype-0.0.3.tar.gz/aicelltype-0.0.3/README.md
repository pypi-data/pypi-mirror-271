# AICelltype
# Installation
You can use pip install package directly.
```
pip install AICelltype
```
However I strongly recommend a virtual environment, if you do not have conda please install Miniconda first.  
```
conda create -n aicelltype_env python=3.10.0
conda activate aicelltype_env
pip install AICelltype
```
# Parameters
tissue_name  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In theory, tissue_name can be any type of biological tissue.  
gene_list  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Identify one cell type for each row in gene_list.  
model  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;One model should be chosen from `['gpt4', 'qwen-max', 'ERNIE-4.0']`.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**gpt4**: annotate cell type through gpt4 (default);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**qwen-max**: annotate cell type through ali qwen model, QWEN_KEY needed, refer to [link](https://help.aliyun.com/zh/dashscope/developer-reference/activate-dashscope-and-create-an-api-key) for a key;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**ERNIE-4.0**: annotate cell type through  baidu qianfan model, API_KEY and SECRET_KEY, refer to [link](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application) for them.
# Usage
```
tissue_name = 'human prostate'
gene_lt = [
    ['KLK3', 'KRT8', 'KLK2', 'MSMB', 'ACPP', 'KLK1', 'KLK4'],
    ['MMRN1', 'FLT4', 'RELN', 'CCL21', 'PROX1', 'LYVE1'],
    ['CD69', 'IL7R', 'CD3D', 'CD3E', 'CD3G', 'ACTA2', 'MYO1B', 'ACTA2', 'ANPEP', 'PDGFRB', 'CSPG4'],
    ['DDX49', 'LOC105371196', 'MTND1P30', 'LOC105373682', 'TAGLN2', 'ZNF836', 'ZNF677', 'COILP1']
]

usage1:
    # gpt4 model
    from AICelltype import aicelltype
    cell_lt = aicelltype(tissue_name, gene_lt, model='gpt4')
    print(cell_lt)
output1:
    ['Prostate Epithelial Cells', 'Lymphatic Endothelial Cells', 'T Cell and Myofibroblast', 'Unknown Cell Type']  # In result, you can get a list with four cell types which have the same order with parameter gene_list.

usage2:
    # qwen-max model
    import os
    os.environ['QWEN_KEY'] = 'your QWEN_KEY'  # Add QWEN_KEY to environ, keep secret to yourself.
    
    from AICelltype import aicelltype
    cell_lt = aicelltype(tissue_name, gene_lt, model='qwen-max')
    print(cell_lt)
output2:
    ['Prostate secretory epithelial cell', 'Lymphatic endothelial cell', 'Immune cell (likely T-cell) and smooth muscle cell mixture', 'Unknown cell type']

usage3:
    # ERNIE-4.0 model
    import os
    os.environ['API_KEY'] = 'your AIP_KEY'  # Add API_KEY to environ, keep secret to yourself.
    os.environ['SECRET_KEY'] = 'your SECRET_KEY'  # Add SECRET_KEY to environ, keep secret to yourself.
    
    from AICelltype import aicelltype
    cell_lt = aicelltype(tissue_name, gene_lt, model='qwen-max')
    print(cell_lt)
output3:
    ['Prostate glandular cells (or Prostate epithelial cells)', 'Lymphatic endothelial cells', 'T-cells (or T-lymphocytes)', 'Unknown cell type (or Possibly cancer-associated cells or Stromal cells; needs further investigation)']  # This model give more explaination.
```


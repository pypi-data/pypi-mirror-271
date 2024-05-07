A collection of useful tools!

## Publish
[quant2 · PyPI](https://pypi.org/project/quant2/)
```sh
# https://github.com/pypa/flit
flit publish
```

## Installation
```sh
pip install -U quant2
pip install -U quant2 -i https://pypi.org/simple
pip install -U quant2 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -U 'git+https://github.com/flystarhe/quant'
```

## Environment
```sh
conda info -e
conda create -y -n myenv python=3.9
conda activate myenv

# pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install notebook

conda deactivate
conda remove -y -n myenv --all
conda info -e
```

## Requirements
```sh
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install scikit-learn simplejson prettytable
```

## Docs
首先安装Python文档生成工具[Sphinx](https://www.sphinx-doc.org/en/master/)，安装指令为`pip install -U sphinx`。

PDF文档依赖：`apt-get update && apt-get install texlive-full`。
PDF文档依赖：`apt-get install texlive-latex-recommended texlive-fonts-recommended texlive-latex-extra`。
PDF文档依赖：`apt-get install texlive-xetex texlive-fonts-recommended texlive-plain-generic`。

- `cd docs`进入文档目录
- `sphinx-quickstart`初始化
- `docs/source/conf.py`完善配置
- `sphinx-apidoc -o source -f -e ..`生成API文档
- `make html/make help`生成文档
- `make clean`清空文档目录

在项目根目录执行时，需要修改文档输出路径及模块路径：
```
sphinx-apidoc -o docs/source -f -e .
```

目录结构如下：
```textile
.
├── Makefile
├── build  # 存放`make html`生成的文档的目录
├── make.bat
└── source  # 存放用于生成文档的源文件
    ├── _static
    ├── _templates
    ├── conf.py  # 配置文件
    └── index.rst
```

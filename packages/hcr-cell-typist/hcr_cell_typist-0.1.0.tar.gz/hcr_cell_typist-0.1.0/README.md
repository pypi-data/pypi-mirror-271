# Cell Typist
A library to aid cell type classification in HCR experiments, downstream of [QuPath](https://qupath.github.io/)

## Installation 
We recommend installing all the required dependencies through [Miniconda](https://docs.conda.io/en/latest/miniconda.html), allowing Cell Typist to run inside a dedicated environment without interfering or causing conflicts with the host computer.

To create a dedicated environment, run the commands below commands inside Anaconda Prompt (on Windows) or a terminal on Linux and macOS.

```bash
(base) $ conda create -n ct python=3.12
(base) $ conda activate ct
```

Afterward, Cell Typist can be installed from PyPi

```bash
(ct) $ pip install hcr-cell-typist
```

This will also install Jupyter, so after installation and activation of the *ct* environment, a jupyter session can be started with

```bash
(ct) $ jupyter notebook
```

## Usage
An example workflow for analysis, covering all the API, can be found [here](https://gitlab.com/NCDRlab/cell-typist/-/blob/main/cell_typist/docs/workflow_analysis.ipynb).

We also provide a [notebook](https://gitlab.com/NCDRlab/cell-typist/-/blob/main/cell_typist/docs/workflow_merging.ipynb) covering merging of results and custom plotting.

## Versions
A changelog with bug fixes and features per version can be found [here](https://gitlab.com/NCDRlab/cell-typist/-/blob/main/CHANGELOG.md)
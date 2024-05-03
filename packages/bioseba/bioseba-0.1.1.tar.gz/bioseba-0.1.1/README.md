# SEBA
conserved Sequence Engineering for the chromatin domain Boundary Architect

## Installation
**Dependency:**
This project requires the GPU environment. Note that the code has only been tested with the specified versions and also expects a Linux environment.

Install the seba via pip.
``` bash
pip install bioseba
```

Then, install the appropriate version of PyTorch. After experimental verification, hiclip works well in the environment of pytorch 2.0.1 + CUDA 11.7.
``` bash
# This is just an example, you can find the appropriate version in https://pytorch.org/get-started/previous-versions/
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117
```

## Quick start for generating CDB sequence
``` bash
# filter out seed sequences suitable for generation
bioseba get-sequence-seed --data_dir_path /path/to/boundary_folder --fasta_path dna.primary_assembly.fa --output_path seed.bed
# generate
bioseba generate-sequence --seed_path seed.bed --output_path sequence.csv
```

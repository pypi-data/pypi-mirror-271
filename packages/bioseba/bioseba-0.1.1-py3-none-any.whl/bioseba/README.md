### Train classifier
``` bash
# data preprocess
python process_finetune_data.py prepross --data_dir_path /lmh_data/data/insulation_score --fasta_path /lmh_data/data/CDBGenerator/5kb/Homo_sapiens.GRCh38.dna.primary_assembly.fa --output_path /lmh_data/data/CDBGenerator/5kb/genome_CDB_dynamic_sequence.bed
# generate train dataset
python process_finetune_data.py create-dataset --file_path /lmh_data/data/CDBGenerator/5kb/genome_CDB_dynamic_sequence.bed --output_path /lmh_data/data/CDBGenerator/5kb/BPE
# train
bash train_classifier.sh
```

### Generate sequence
``` bash
# filter out seed sequences suitable for generation
python generator.py get-sequence-seed --data_dir_path /lmh_data/data/boundary --fasta_path /lmh_data/data/CDBGenerator/5kb/Homo_sapiens.GRCh38.dna.primary_assembly.fa --output_path /lmh_data/data/CDBGenerator/5kb/generator/seed.bed
# generate
python generator.py generate-sequence --seed_path /lmh_data/data/CDBGenerator/5kb/generator/seed.bed --output_path output/insulated_sequence.csv
```
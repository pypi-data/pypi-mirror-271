# PFEX - Python Fisher EXact

The Python Fisher Exact test package supports EnrichR libraries and mimics the EnrichR backend. It has high performance for large gene set libraries. Instant enrichment results for a pure Python implementation of the Fisher Exact Test. This implementation allows the calculation of the same p-values as the Enrichr API, but runs locally and results in faster p-value computation.

### Installation

Install Python library using pip directly from Github. The repository is currently private.

```
pip3 install git+https://<token>:x-oauth-basic@github.com/maayanlab/pfx.git
```

Replace <token> with the Github token allowing access. You can generate an access token in Github by selecting Profile (top right -> Settings -> Developer Settings -> Personal Access Tokens)


### Enrichment Analysis

To run PFEX in Python run the following command. The result will be a dataframe containing the enriched gene sets of the library as rows, sorted by p-value.

```python
import pfex as pfx

# list all libraries from Enrichr
libraries = pfx.libraries.list_libraries()

# load a gene set library
lib = pfx.libraries.get_library("GO_Biological_Process_2023")

# get example gene set
gene_set = pfx.libraries.example_set()

# calculate enrichment for gene set against all gene sets in library
result = pfx.enrichment.fisher(gene_set, lib)
```

`lib` is a dictionary of sets. `pfx.enrichment.fisher` expects as input a set (gene_set) and a library (lib) in the form of a dictionary of sets.

### Example Output

The results are returned as Pandas DataFrames. The columns contain term, p-value, Sidak multiple hypothesis corrected p-value (sidak), False Discovery Rate (fdr), odds ratio (odds), overlap size (overlap), set-size, and gene-overlap.

| #  | Term                                                       | p-value       | sidak          | fdr           | odds      | overlap | set-size | Gene-overlap                                                                                         |
|--- |------------------------------------------------------------|---------------|----------------|---------------|-----------|---------|----------|------------------------------------------------------------------------------------------------------|
| 1  | Regulation Of Cell Population Proliferation...              | 1.041581e-41  | 5.655786e-39   | 5.655786e-39  | 8.903394  | 62      | 766      | PDGFRB,TGFB2,CSF1R,CXCL10,CD86,IL4,CTNNB1,STAT...                                                    |
| 2  | Positive Regulation Of Cell Population Proliferation...     | 2.914662e-37  | 1.582661e-34   | 7.913307e-35  | 11.159420 | 49      | 483      | PDGFRB,TGFB2,CSF1R,CD86,IL4,AKT1,EGFR,JAK2,CDK...                                                    |
| 3  | Positive Regulation Of Cell Migration (GO:0030335)          | 1.929354e-35  | 1.047639e-32   | 3.492131e-33  | 15.772059 | 39      | 272      | PDGFRB,TGFB2,CSF1R,ATM,PECAM1,TWIST1,IL4,STAT3...                                                    |
| 4  | Regulation Of Apoptotic Process (GO:0042981)                | 9.892051e-34  | 5.371384e-31   | 1.342846e-31  | 8.269504  | 53      | 705      | CASP9,CXCL10,ATM,RPS6KB1,FAS,IL4,CTNNB1,CD28,A...                                                    |
| 5  | Positive Regulation Of Intracellular Signal Transmission... | 3.297600e-33  | 1.790597e-30   | 3.581194e-31  | 9.847619  | 47      | 525      | PDGFRB,TGFB2,CD86,CHI3L1,BECN1,ENG,GAPDH,PPARG...                                                    |


### Fisher Initialization

When multiple libraries are computed some calculations can be pre initialized. This will speed up overall execution time.

```python
import pfex as pfx

# initialize calculations
fisher = pfx.enrichment.FastFisher(34000)

# load a gene set library
lib_1 = pfx.libraries.get_library("GO_Biological_Process_2023")
lib_2 = pfx.libraries.get_library("KEGG_2021_Human")

# get example gene set
gene_set = pfx.libraries.example_set()

# calculate enrichment for gene set against all gene sets in library 1 and 2
result_1 = pfx.enrichment.fisher(gene_set, lib_1, fisher=fisher)
result_2 = pfx.enrichment.fisher(gene_set, lib_2, fisher=fisher)
```

### Gene Set Filtering

Small gene sets and small overlaps can be filtered using the parameters `min_set_size` and `min_overlap`.

```python
import pfex as pfx

# load a gene set library
lib = pfx.libraries.get_library("GO_Biological_Process_2023")

# get example gene set
gene_set = pfx.libraries.example_set()

# calculate enrichment for gene set against all gene sets in library.
# Only gene sets larger than 10 genes are used and the minimum overlap has to be at least 5 to be reported.
result = pfx.enrichment.fisher(gene_set, lib, min_set_size=10, min_overlap=5)
```


### Enrichment of Gene Set Library vs Gene Set Library

When computing enrichment for multiple gene sets against a gene set library PFEX uses an optimized implementation of overlap detection and multithreading to increase computational speed. In the example below we compute all pairwise enrichment between gene sets in GO Biological Processes. As before it is calling the fisher function, but instead of a gene set as first parameter it receives a gene set library in dictionary format. The output is a list of results containing a result dataframe for each gene set vs gene set library. The results can be consolidated into a single p-value matrix.

```python
import pfex as pfx

# load a gene set library
lib = pfx.libraries.get_library("GO_Biological_Process_2023")

# calculate enrichment for gene set library against all gene sets in another library.
# Only gene sets larger than 10 genes are used and the minimum overlap has to be at least 5 to be reported.
result = pfx.enrichment.fisher(lib, lib, min_set_size=10, min_overlap=5)

# consolidate all p-values into a single dataframe
pmat = pfx.enrichment.consolidate(result)
```



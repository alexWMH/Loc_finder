# Loc_finder

A lightweight Python tool designed to quickly search and extract specific genomic positions from a compressed VCF file (`.vcf.gz`).

> [!IMPORTANT]
> **Prerequisites Before You Start:**
> 1. **`vcf.gz` file**: The target compressed VCF file you want to search. (You can't search without an input file, right?)
> 2. **`vcf.tbi` file**: This index file is **required** for fast querying. If you don't have it, please generate it using `tabix` before running the script:
>    ```bash
>    tabix -p vcf /path/to/your/file.vcf.gz
>    ```

---

## Usage 
### Basic Command
```bash
python loc_finder.py -vcf <path_to_vcf> -loc <path_to_loc_txt> [-o <output_prefix>]
```
### Options:
`-h`, `--help`           show this help message and exit
`-vcf`, `--vcf_file`     input VCF.gz file path.
`-loc`, `--loc_file`     txt file for location find (e.g., 15:61978566).
`-o`, `--output_prefix`  out put vcf name, Default: output.

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
python loc_finder.py -vcf <path_to_vcf> -loc <path_to_loc_txt> -o <output_prefix>
```
### Options:
| Options | Description |
| :--- | :--- |
| `-h`, `--help` | Show this help message and exit. |
| `-vcf`, `--vcf_file` | Input VCF.gz file path. |
| `-loc`, `--loc_file` | Txt file for location find (e.g., 15:61978566). |
| `-o`, `--output_prefix` | Output VCF name. (Default: `output`) |

#### loc file
Search location file  
> [!Note]
> location file need contain specific formate

locations.txt example:
**Single position**
```text
15:61978566
M:16162
...
```

**Region position (Full format)**
```text
12:20850365-12:20860041
...
```

**Region position (Shortcut format)**
```text
12:20850365-20860041
...
```

## Output file 
| Output file | Description |
| :--- | :--- |
| `.log` | Program log and execution details. |
| `_find.txt` | Text file containing summary results of whether each location was found. |
| `.vcf` | Filtered VCF file containing all the successfully extracted genomic locations. |

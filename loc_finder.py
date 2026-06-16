import argparse
import os
import sys
import pysam

def parse_args():
    parser = argparse.ArgumentParser(description="  ===== Multiple VCF Location Finder =====  ", formatter_class=argparse.RawTextHelpFormatter,)
    parser.add_argument("-vcf", "--vcf_file", required=True, metavar="", help="input VCF.gz file path.")
    parser.add_argument("-loc", "--loc_file", required=True, metavar="", help="txt file for location find (e.g., 15:61978566).")
    parser.add_argument("-o", "--output_prefix", default="output", metavar="", help="out put vcf name, Default: output.",)
    return parser.parse_args()

def load_loci(loc_file):
    """
    load loc.txt and record find location
    Support format below:
    Support format below:
    - single pos: 15:61978566
    - region pos: 12:20850365-12:20860041
    - region pos: 12:20850365-20860041

    return: (origin string, chromosome, start_pos, end_pos, is_region)
    """
    loci = []
    if not os.path.exists(loc_file):
        print(f"Error: location file not found: {loc_file}")
        sys.exit(1)

    with open(loc_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "-" in line:
                # processing region 
                try:
                    chrom_part, end_part = line.split("-")
                    # processing chrom_part (Ex. 12:20850365)
                    chrom, start_pos = chrom_part.split(":")
                    
                    # processing end_part, if 12:20860041 split again; if  20860041 don't split 
                    if ":" in end_part:
                        _, end_pos = end_part.split(":")
                    else:
                        end_pos = end_part
                        
                    loci.append((line, chrom.strip(), int(start_pos.strip()), int(end_pos.strip()), True))
                except Exception:
                    print(f"[Warrning] Can't splt string format: {line}")
            else:
                if ":"  in line:
                    chrom, pos = line.split(":", 1)
                    try:
                        p = int(pos.strip())
                        loci.append((line, chrom.strip(), p, p, False))
                    except ValueError:
                        continue
    return loci

def main():
    args = parse_args()
    out_vcf_path = f"{args.output_prefix}.vcf"
    out_find_path = f"{args.output_prefix}_find.txt"
    out_log_path = f"{args.output_prefix}.log"

    # check tbi file exists
    if not os.path.exists(args.vcf_file + ".tbi"):
        # some tbi file name does't contain .gz, also check .vcf.tbi  
        alt_tbi = args.vcf_file.replace(".gz", ".tbi")
        if not os.path.exists(alt_tbi):
            print(
                f"Error: vcf index file not found (.tbi) Please run command: tabix -p vcf {args.vcf_file} first.")
            sys.exit(1)
    
    loci_list = load_loci(args.loc_file)

    # Using tbi to search vcf file 
    try:
        tbx = pysam.TabixFile(args.vcf_file)
    except Exception as e:
        print(f"Can't read vcf file: {e}")

    # get vcf header to check chromosome name
    vcf_chroms = list(tbx.contigs)
    #records = tbx.fetch("chrM", 16150, 16170)
    #for r in records:
    #    print(r)

    with open(out_vcf_path, "w") as out_vcf, open(out_find_path, "w") as out_find, open(out_log_path, "w") as out_log:
        for header_line in tbx.header:
            # write header line
            out_vcf.write(header_line + "\n") 
            # catch loc
        for orig_str, chrom, start_pos, end_pos, is_region in loci_list:
            # fix chromosome name (ex. 15 -> chr15 or M -> chrM)
            target_chrom = chrom
            if chrom not in vcf_chroms:
                if f"chr{chrom}" in vcf_chroms:
                    target_chrom = f"chr{chrom}"
                elif chrom.startswith("chr") and chrom[3:] in vcf_chroms:
                    target_chrom = chrom[3:]
                else:
                    out_find.write(f"{orig_str}\t not found\n")
                    out_log.write(f"chromosome {chrom} not found in vcf file.\n")
                    print(f"chromosome {chrom} not found.")
                    continue

            found_any = False
            try:
                # tabix is 0-base started
                records = tbx.fetch(target_chrom, start_pos-1 ,end_pos)
                #print(records)
                for record in records:
                    flelds = record.split("\t")
                    vcf_pos = int(flelds[1])
                    
                    if start_pos <= vcf_pos <= end_pos:
                        out_vcf.write(record + "\n")
                        found_any = True
            except ValueError as e:
                #  fetch error（ex. pos > chromosome length）
                out_log.write(
                    f"[ERROR] pos error {orig_str}: {str(e)}\n"
                )
            except Exception as e:
                out_log.write(
                    f"[ERROR] Unknow error {orig_str}: {str(e)}\n"
                )
            
            # load find.txt
            if found_any:
                out_find.write(f"{orig_str}\tfound\n")
            else:
                out_find.write(f"{orig_str}\tnot found\n")
    
    
    print(f"Search finished！")
    print(f"  - VCF result: {out_vcf_path}")
    print(f"  - find txt: {out_find_path}")
    print(f"  - error log: {out_log_path}")
       
if __name__ == "__main__":
    main()

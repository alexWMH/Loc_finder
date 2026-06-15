# Loc_finder
This tools is to help you find specific position in vcf.gz file 

> [!IMPORTANT]
> Before we start you will need this file 
> vcf.gz file as we need to search specific location in this you can't find file with out input right lol~
> vcf.tbi file this file help us to find loc fast so if you don't have this file please run: tabix -p vcf [path/to/your/vcf.gz/file]

## Option 
Basic usage:
'''
python loc_finder.py [-h] -vcf  -loc  [-o]
'''
Options:
'-h', '--help'           show this help message and exit
'-vcf', '--vcf_file'     input VCF.gz file path.
'-loc', '--loc_file'     txt file for location find (e.g., 15:61978566).
'-o', '--output_prefix'  out put vcf name, Default: output.

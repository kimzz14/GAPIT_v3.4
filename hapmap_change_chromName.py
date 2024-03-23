from optparse import OptionParser
import sys
#option parser
parser = OptionParser(usage="""Run annotation.py \n Usage: %prog [options]""")
parser.add_option("-i","--input",action = 'store',type = 'string',dest = 'INPUT',help = "")
parser.add_option("-o","--output",action = 'store',type = 'string',dest = 'OUTPUT',help = "")
(opt, args) = parser.parse_args()
if opt.INPUT == None or opt.OUTPUT == None:
    print('Basic usage')
    print('')
    print('     python hapmap_change_chromName.py -i input.hmp.txt -o input.chrom.hmp.txt')
    print('')
    sys.exit()

infile = opt.INPUT
outfile = opt.OUTPUT

fin = open(infile)

fout = open(outfile, 'w')

chrom_DICT = {}
fout.write(fin.readline())
for line in fin:
    mylist = line.rstrip('\n').split('\t')
    chrom = mylist[2]
    if not chrom in chrom_DICT:
        chrom_DICT[chrom] = 1 + len(chrom_DICT.keys())
    mylist[2] = str(chrom_DICT[chrom])
    fout.write('\t'.join(map(str, mylist)) + '\n')
fout.close()


import os

class PhenotypeTab:
    def __init__(self, fileName):
        fin = open(fileName)
        legend_LIST = fin.readline().rstrip('\n').split('\t')
        fields_LIST = []
        for line in fin:
            data_LIST = line.rstrip('\n').split('\t')
            fields = {key:value for key, value in zip(legend_LIST, data_LIST)}
            fields_LIST += [fields]
        fin.close()
        self.fields_LIST = fields_LIST
        self.legend_LIST = legend_LIST
    def makeFile(self, fileName, taxa_DICT, phenotype):
        taxa_LIST = []
        fout = open(fileName, 'w')
        fout.write('\t'.join(['Taxa', phenotype]) + '\n')
        for fields in self.fields_LIST:
            phenoValue = fields[phenotype]
            if phenoValue == 'NA':
                continue

            taxa = fields['Taxa']
            if not taxa in taxa_DICT:
                continue
            
            taxa_LIST += [taxa]
            fout.write(taxa + '\t' + phenoValue + '\n')
        fout.close()
        return taxa_LIST
    
class GenotypeTab:
    def __init__(self, fileName):
        fin = open(fileName)
        legend_LIST = fin.readline().rstrip('\n').split('\t')
        self.fileName = fileName
        self.legend_LIST = legend_LIST
        self.legend_DICT = {legend:0 for legend in legend_LIST}
    def makeFile(self, fileName, legend_LIST):
        idx_LIST = [self.legend_LIST.index(legend) for legend in legend_LIST]

        fin = open(self.fileName)
        fin.readline()
        fout = open(fileName, 'w')
        fout.write('\t'.join(legend_LIST) + '\n')
        for line in fin:
            data_LIST = line.rstrip('\n').split('\t')
            context = [data_LIST[idx] for idx in idx_LIST]
            fout.write('\t'.join(context) + '\n')
        fout.close()

command_GAPIT = """options(repos = c(CRAN = "https://cloud.r-project.org/"))
source("../../GAPIT_v3.4/gapit_functions.txt")
myY <- read.table("phenotype.txt", head=TRUE)
myG <- read.table("genotype.hmp.txt", head=FALSE)
myGAPIT <- GAPIT(Y=myY, G=myG, PCA.total=3, model=c("Blink", "FarmCPU", "gBLUP", "sBLUP", "cBLUP", "SUPER", "MLMM", "CMLM", "MLM", "GLM"),Multiple_analysis=TRUE, Inter.Plot=TRUE)
q()
"""


prefix = 'GAPIT'
if os.path.isdir(prefix) == True:
    print("exist directory")
    raise SystemExit(-1)
os.mkdir(prefix)

phenotypeFile = 'phenotype.txt'
genotypeFile = 'genotype.hmp.txt'

phenotypeTab = PhenotypeTab(phenotypeFile)
genotypeTab = GenotypeTab(genotypeFile)


fout_all = open('run.sh', 'w')
for phenotype in phenotypeTab.legend_LIST[1:]:
    #make directory
    os.mkdir(prefix + '/' + phenotype)
    
    #phenotype File
    taxa_LIST = phenotypeTab.makeFile(prefix + '/' + phenotype + '/' + phenotypeFile, genotypeTab.legend_DICT, phenotype)

    #genotype File
    genotypeTab.makeFile(prefix + '/' + phenotype + '/' + genotypeFile, ['rs', 'alleles', 'chrom', 'pos', 'strand', 'assembly', 'center', 'protLSID', 'assayLSID', 'panelLSID', 'QCcode'] + taxa_LIST)

    #run_GAPIT.r
    fout = open(prefix + '/' + phenotype + '/' + 'run_GAPIT.r', 'w')
    fout.write(command_GAPIT)
    fout.close()

    #run.sh
    fout = open(prefix + '/' + phenotype + '/' + 'run.sh', 'w')
    fout.write('cd' + ' ' + prefix + '/' + phenotype + '\n')
    fout.write('Rscript --verbose run_GAPIT.r 1> run.log 2> run.err')
    fout.close()

    #all
    fout_all.write('sh' + ' ' + prefix + '/' + phenotype + '/' + 'run.sh' + '\n')
fout_all.close()

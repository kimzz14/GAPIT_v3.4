import os

command_GAPIT = """options(repos = c(CRAN = "https://cloud.r-project.org/"))
source("../../GAPIT_v3.4/gapit_functions.txt")
myY <- read.table("phenotype.txt", head=TRUE)
myG <- read.table("../../genotype.hmp.txt", head=FALSE)
myGAPIT <- GAPIT(Y=myY, G=myG, PCA.total=3, model=c("GLM", "MLM", "CMLM", "MLMM","SUPER", "FarmCPU", "gBLUP", "cBLUP", "sBLUP", "Blink"),Multiple_analysis=TRUE, Inter.Plot=TRUE)
q()
"""


phenotypeFile = 'phenotype.txt'

prefix = 'GAPIT'

fin = open(phenotypeFile)

legend_LIST = fin.readline().rstrip('\n').split('\t')
fields_LIST = []
for line in fin:
    data_LIST = line.rstrip('\n').split('\t')
    fields = {key:value for key, value in zip(legend_LIST, data_LIST)}
    fields_LIST += [fields]
fin.close()


if os.path.isdir(prefix) == True:
    print("exist directory")
    raise SystemExit(-1)

os.mkdir(prefix)
fout_all = open('run.sh', 'w')
for phenotype in legend_LIST[1:]:
    os.mkdir(prefix + '/' + phenotype)
    fout = open(prefix + '/' + phenotype + '/' + phenotypeFile, 'w')
    fout.write('Taxa' + '\t' + phenotype + '\n')
    for fields in fields_LIST:
        fout.write(fields['Taxa'] + '\t' + fields[phenotype] + '\n')
    fout.close()

    fout = open(prefix + '/' + phenotype + '/' + 'run_GAPIT.r', 'w')
    fout.write(command_GAPIT)
    fout.close()

    fout = open(prefix + '/' + phenotype + '/' + 'run.sh', 'w')
    fout.write('cd' + ' ' + prefix + '/' + phenotype + '\n')
    fout.write('Rscript --verbose run_GAPIT.r 1> run.log 2> run.err')
    fout.close()
    fout_all.write('sh' + ' ' + prefix + '/' + phenotype + '/' + 'run.sh' + '\n')
fout_all.close()

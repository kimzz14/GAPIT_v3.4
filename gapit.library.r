options(repos = c(CRAN = "https://cloud.r-project.org/"))
install.packages("ape")
install.packages("bigmemory")
install.packages("compiler")
install.packages("EMMREML")
install.packages("genetics")
install.packages("gplots")
install.packages("grid")
install.packages("htmltools")
install.packages("lme4")
install.packages("manipulateWidget")
install.packages("rgl")
install.packages("scatterplot3d")
install.packages("BiocManager")
install.packages("plotly")
BiocManager::install("multtest", force=TRUE)
BiocManager::install("snpStats", force=TRUE)
# setwd('../../Matrices/')

# install.packages("Matrix")

## Collect arguments
args <- commandArgs(TRUE)
parseArgs <- function(x) strsplit(sub("^--", "", x), "=")
argsDF <- as.data.frame(do.call("rbind", parseArgs(args)))
argsL <- as.list(as.character(argsDF$V2))
names(argsL) <- argsDF$V1


setwd('/u/flashscratch/d/datduong/simDEF/simDEF_Code/Matrices')
library(methods)
library(Matrix)

######################################
############ PMI Function ############
PMI<-function(x){
	m <- Matrix(0, dim(x)[1], dim(x)[2]) +log10((rowSums(x)+ dim(x)[2]))
	cat("Done with the rows add\n")

	n <- t( t(Matrix(0, dim(x)[1], dim(x)[2])) + log10((colSums(x)+ dim(x)[1])) )
	cat("Done with the columns add\n")

	pmi<-log10(((x+1)*(sum(x)+dim(x)[1]*dim(x)[2])))-(m+n)
	return(pmi)
}
######################################


######################################
##### Matrix Normalizer Function #####
MatrixNorm<-function(m){
	m_rs <- 1/(sqrt(rowSums(m*m)))
	v <- Diagonal(n= length(m_rs), m_rs)
	out <- v%*%m
	return(out)
}
######################################


######################################
### Load MEDLINE first order and MF definition matrices
FOC <- readMM(file='/u/flashscratch/d/datduong/simDEF/simDEF_Code/Matrices/First_Order_Matrix.mtrx') ###  WARNING: make sure your matrix is for R not MATLAB
FOC <- FOC + t(FOC)	### Converts a bigram matrix to a co-occurrence matrix

# 'MF_Definition_Matrix.mtrx'
MF_DEF <- readMM(argsL$defMatrix) ###  WARNING: make sure your matrix is for R not MATLAB
### Initial matrices are loaded now!
######################################
# print (MF_DEF[1:10,1:10])

######################################
### Here we start to build SOC matrix for MF
# print ( dim(MF_DEF) ) # 10842 2033372
# print ( dim(FOC) ) # 2033372 2033372

SOC <- MF_DEF%*%FOC;
a <- rowSums(SOC)
a <- 1/a
D <- Diagonal(n= length(a), a)
SOC <- D%*%SOC
SOC <- SOC[,colSums(SOC)!=0]
rm (D, a, FOC, MF_DEF)
### Now we have SOC matrix for MF
######################################


######################################
### Here we apply PMI on MF SOC matrix
PMI_on_SOC <- PMI(SOC)
rm (SOC)
### PMI applied on MF SOC matrix
######################################


######################################
### Applying cut-off threshold to find better features
DOWN_CUT <- 0;	### change this value for differet cutt-off points from down
TOP_CUT <- 100;	### change this value for differet cutt-off points from top
PMI_on_SOC[which(PMI_on_SOC < DOWN_CUT)] <- 0;
PMI_on_SOC[which(TOP_CUT < PMI_on_SOC)] <- 0;
PMI_on_SOC <- PMI_on_SOC[,colSums(PMI_on_SOC)!=0]
### Cut-off applied on the MF PMI_on_SOC matrix
######################################


######################################
### Compute semantic similarity of MF GO terms (cosine similarity)
PMI_on_SOC <- MatrixNorm(PMI_on_SOC)
simDEF <- PMI_on_SOC%*%(t(PMI_on_SOC)) ### Now we have semantic similarity of MF GO terms
### simDEF is now ready to be used or examined
######################################

nameLabel = read.table ( argsL$labelName, sep=":",header=F, colClasses='character')
simDEF = as.data.frame(as.matrix(simDEF))
write.table(simDEF, file = argsL$saveName, col.names = nameLabel$V1, row.names=FALSE,sep=",")



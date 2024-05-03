#library(RaudioUtils)

#Rscript /home/sam/tmp/audioProcess/an.R [resTable]
args <- commandArgs(TRUE)
dataFile <- args[1]




plotFile <- paste(strsplit(x=dataFile, split='.', fixed=TRUE)[[1]][1], '.pdf', sep='')

dats <- read.table(dataFile, header=TRUE, sep=';')
dats <-  dats[with(dats, order(Ear.,Frequency..Hz.)),]

datsRight <- dats[dats$Ear. == "Right",]
datsLeft <- dats[dats$Ear. == "Left",]

datsKillion <- c(21.7, 15.5, 9.5, 13.9, 15.5)

tRight <- datsRight$threshold_arithmetic - datsKillion
tLeft <- datsLeft$threshold_arithmetic - datsKillion
ymin <- min(c(tRight, tLeft))
ymax <- max(c(tRight, tLeft))

pdf(plotFile)
plot.new(); plot.window(xlim=log10(c(250, 4000)), ylim=c(ymin-1, ymax+1))
lines(log10(datsRight$Frequency..Hz.), tRight, type='b', col='red')
lines(log10(datsLeft$Frequency..Hz.), tLeft, type='b', col='blue')
abline(h=20, lty=2)
grid()
axis(1, at=log10(datsRight$Frequency..Hz.), labels=as.character(datsRight$Frequency..Hz.))
axis(2)
legend("topleft", legend=c("Right", "Left"), col=c("red", "blue"), pch=c(1,1))
title(main=dats$listener[1], xlab="Frequency", ylab="Threshold (dB HL)")
box()
dev.off()

cmd <- paste('mupdf', plotFile)
system(cmd, wait=FALSE)


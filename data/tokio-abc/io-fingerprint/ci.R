lats <- scan("samples.dat")

summary(lats)

library(boot) # Calling boot library
boot.median<-function(x,i){median(x[i])} #defining median function
median.boot<-boot(lats, boot.median, R=10000) # applying bootstrap
median.boot 

boot.ci(median.boot,type="bca")


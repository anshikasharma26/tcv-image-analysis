library(ggplot2)
library(ggridges)
library(reshape2)
library(dplyr)

# Hue plotting function
hue_analysis = function(file, outdir) {
  # read in the data
  data = read.table(file = file, sep = "\t", header = TRUE)
  # create a normalized counts column
  data$norm = data$count/data$total
  # average the normalized counts over the replicates
  data.ave = data %>% group_by(genotype, treatment, timepoint, hue) %>% summarize(density.mean = mean(norm))
  # Reorder treatment factor labels
  data.ave$treatment = factor(data.ave$treatment, levels = c("M", "wt", "CPB"))
  # make a plot for each genotype
  for (genotype in levels(data.ave$genotype)) {
    # Subset the data by genotype
    input = data.ave[data.ave$genotype == genotype,]
    # Create a ggridges plot
    genotype_plot = ggplot(input, aes(x = hue, 
                                      y = factor(timepoint, 
                                                 levels = c(-1, 1, 3, 5, 7, 9, 11, 13, 15, 17)), 
                                      height = density.mean)) + 
      # create the density curves, color by treatment group
      geom_density_ridges2(stat = "identity", aes(fill=treatment), alpha=0.5) +
      # relabel the x-axis
      scale_x_continuous("Hue (degrees)", expand = c(0.01, 0), limits = c(0,100),
                         breaks = c(0, 25, 50, 75, 100), labels = c(0, 50, 100, 150, 200)) + 
      scale_y_discrete("Days post infection", expand = c(0.01, 0)) + 
      ggtitle(genotype) +
      theme_bw() +
      theme_ridges() + 
      theme(axis.title = element_text(face="bold"))
    ggsave(filename = paste(outdir, paste(genotype, ".ridges.pdf", sep = ""), sep = "/"))
  }
  
  # make a plot for each genotype x treatment group
  for (genotype in levels(data.ave$genotype)) {
    for (treatment in levels(factor(data.ave$treatment))) {
      # Subset the data by genotype and treatment
      input = data.ave[data.ave$genotype == genotype & data.ave$treatment == treatment,]
      # Create a ggridges plot
      gxt_plot = ggplot(input, aes(x = hue, 
                                   y = factor(timepoint, levels = c(-1, 1, 3, 5, 7, 9, 11, 13, 15, 17)), 
                                   height = density.mean)) + 
        # create the density curves, color by hue
        geom_density_ridges_gradient(stat = "identity", aes(fill=..x..)) + 
        scale_fill_gradientn(colours = rainbow(180)) +
        # relabel the x-axis
        scale_x_continuous("Hue (degrees)", expand = c(0.01, 0), 
                           breaks = c(0, 50, 100, 150), labels = c(0, 100, 200, 300)) + 
        scale_y_discrete("Days post infection", expand = c(0.01, 0)) + 
        ggtitle(paste(genotype, "+", treatment, sep = " ")) +
        theme_bw() +
        theme_ridges() + 
        theme(axis.title = element_text(face="bold"))
      ggsave(filename = paste(outdir, paste(genotype, treatment, "hue-plot.pdf", sep = "-"), sep = "/"))
    }
  }
}

# Pilot dataset with Col-0 and the dcl234 triple mutant
hue_analysis(file = "./results/pilot/pilot_arabidopsis-tcv-hue-histograms.txt", outdir = "./plots/pilot")

# Complete dataset with Col-0, the dcl234 triple mutant, and ago1 through 10 single mutants
hue_analysis(file = "./results/complete/complete_arabidopsis-tcv-hue-histograms.txt", outdir = "./plots/complete")


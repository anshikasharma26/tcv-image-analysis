# PlantCV-based Image Analysis of Arabidopsis Infection with TCV

## Image Analysis with PlantCV

### Parallelization with HTCondor

The script `parallel-plantcv-arabidopsis-tcv.py` was used to create an HTCondor job cluster submission file. The script
walks through an input directory of images and creates a job for each image using the `plantcv-arabidopsis-tcv-image.py`
script as the executable. 

```
usage: parallel-plantcv-arabidopsis-tcv.py [-h] --dir DIR --pdfs PDFS --outdir
                                           OUTDIR --jobfile JOBFILE
                                           [--debug DEBUG]

Create an HTCondor job to process Arabidopsis images infected with TCV.

optional arguments:
  -h, --help         show this help message and exit
  --dir DIR          Directory containing images. (default: None)
  --pdfs PDFS        Naive Bayes PDF file. (default: None)
  --outdir OUTDIR    Output directory for images. (default: None)
  --jobfile JOBFILE  Output HTCondor job file. (default: None)
  --debug DEBUG      Activate debug mode. Values can be None, 'print', or
                     'plot' (default: None)
```

The script `plantcv-arabidopsis-tcv-image.py` is a PlantCV (http://plantcv.danforthcenter.org) analysis script. For each
input image it outputs an image with plant pixels classified as "healthy" or "unhealthy" and an image with these classes
transparently overlaid onto the original image. It also outputs several text files per image that can be concatenated
to produce output tables for hue histograms, general hue statistics, and 1-, 2-, and 3-component Gaussian Mixture 
Models.

```
usage: plantcv-arabidopsis-tcv-image.py [-h] --image IMAGE --pdfs PDFS
                                        --outfile OUTFILE --outdir OUTDIR
                                        [--debug DEBUG]

Process Arabidopsis images infected with TCV.

optional arguments:
  -h, --help         show this help message and exit
  --image IMAGE      An image file. (default: None)
  --pdfs PDFS        Naive Bayes PDF file. (default: None)
  --outfile OUTFILE  Output text filename. (default: None)
  --outdir OUTDIR    Output directory for images. (default: None)
  --debug DEBUG      Activate debug mode. Values can be None, 'print', or
                     'plot' (default: None)
```

After the hue histogram data is concatenated into a single table, the R script `hue_analysis.R` was used to generate
ridgeline plots for the pilot (Col-0 and dcl234) and complete (Col-0, dcl234, and ago1 through 10 single mutants).

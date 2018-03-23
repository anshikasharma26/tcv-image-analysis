#!/usr/bin/env python

import os
import argparse
import plantcv as pcv
import numpy as np


def options():
    parser = argparse.ArgumentParser(description="Process Arabidopsis images infected with TCV.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--image", help="An image file.", required=True)
    parser.add_argument("--pdfs", help="Naive Bayes PDF file.", required=True)
    parser.add_argument("--outfile", help="Output text filename.", required=True)
    parser.add_argument("--debug", help="Activate debug mode. Values can be None, 'print', or 'plot'", default=None)

    args = parser.parse_args()

    if not os.path.exists(args.image):
        raise IOError("The image {0} does not exist!".format(args.image))

    return args


def main():
    # Parse command-line options
    args = options()

    device = 0

    # Open output file
    out = open(args.outfile, "w")

    # Open the image file
    img, path, fname = pcv.readimage(filename=args.image, debug=args.debug)
    # Classify healthy and unhealthy plant pixels
    device, masks = pcv.naive_bayes_classifier(img=img, pdf_file=args.pdfs, device=device)
    # Fill small objects
    device, fill_image_healthy = pcv.fill(img=np.copy(masks["Healthy"]), mask=np.copy(masks["Healthy"]),
                                          size=300, device=device, debug=args.debug)
    device, fill_image_unhealthy = pcv.fill(img=np.copy(masks["Unhealthy"]), mask=np.copy(masks["Unhealthy"]),
                                            size=1000, device=device, debug=args.debug)
    # Define a region of interest
    device, roi1, roi_hierarchy = pcv.define_roi(img=img, shape='rectangle', device=device, roi=None,
                                                 roi_input='default', debug=args.debug, adjust=True, x_adj=1100,
                                                 y_adj=450, w_adj=-970, h_adj=-570)
    # Filter objects that overlap the ROI
    device, id_objects, obj_hierarchy_healthy = pcv.find_objects(img=img, mask=fill_image_healthy,
                                                                 device=device, debug=args.debug)
    device, _, _, kept_mask_healthy, _ = pcv.roi_objects(img=img, roi_type='partial', roi_contour=roi1,
                                                         roi_hierarchy=roi_hierarchy, object_contour=id_objects,
                                                         obj_hierarchy=obj_hierarchy_healthy, device=device,
                                                         debug=args.debug)
    device, id_objects, obj_hierarchy_unhealthy = pcv.find_objects(img=img, mask=fill_image_unhealthy,
                                                                   device=device, debug=args.debug)
    device, _, _, kept_mask_unhealthy, _ = pcv.roi_objects(img=img, roi_type='partial', roi_contour=roi1,
                                                           roi_hierarchy=roi_hierarchy,
                                                           object_contour=id_objects,
                                                           obj_hierarchy=obj_hierarchy_unhealthy, device=device,
                                                           debug=args.debug)
    # Combine the healthy and unhealthy mask
    device, mask = pcv.logical_or(img1=kept_mask_healthy, img2=kept_mask_unhealthy, device=device,
                                  debug=args.debug)

    # Extract hue values from the image
    device, h = pcv.rgb2gray_hsv(img=img, channel="h", device=device, debug=args.debug)

    # Extract the plant hue values
    plant_hues = h[np.where(mask == 255)]

    # Initialize hue histogram
    hue_hist = {}
    for i in range(0, 180):
        hue_hist[i] = 0

    # Populate histogram
    total_px = len(plant_hues)
    for hue in plant_hues:
        hue_hist[hue] += 1

    # Parse the filename
    genotype, treatment, replicate, timepoint = args.image[:-4].split("_")
    replicate = replicate.replace("#", "")
    if timepoint[-3:] == "dbi":
        timepoint = -1
    else:
        timepoint = timepoint.replace("dpi", "")

    # Output results
    for i in range(0, 180):
        out.write("\t".join(map(str,
                                [genotype, treatment, timepoint, replicate, total_px, i, hue_hist[i]])) + "\n")
    out.close()


if __name__ == '__main__':
    main()

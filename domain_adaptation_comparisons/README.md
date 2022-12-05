# Generating images produce by other domain adaptation techniques

1. CycleGAN and Cycada

We used the repository [https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix] (https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix) with the addition of defining a dataset specific to our use case which you can find in this directory: wt.py. CycleGAN and Cycada were trained using their base settings for 200 epochs each. Since our experiments assumed a data-scarce scenario with minimal access to source domain labels, we used 100 background images and the 100 base real labeled images as our Domain A and 100 background images as Domain B sets.

2. Histogram equalization and Grayworld

Found in script CE_plus_GW.py. 

We ended up using the "domain" settings as opposed to the "single" settings. The domain settings aggregate domain-wide info of the sets of 100 train images we used (aka use the summed information) to create mappings, whereas single paired individual photos and thus generated unique mappings based off only one image.

3. Histogram matching

TODO





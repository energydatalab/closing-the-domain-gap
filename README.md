# Closing the domain gap

Welcome to our github! Here you can find code documentation for our 2022 Neurips CCAI submission 'Closing the Domain Gap -- Blended Synthetic Imagery for Climate Object Detection'. This includes our dataset, experiments, and synthetic image generation. Here is a [link](https://www.climatechange.ai/papers/neurips2022/37) to the full workshop paper.

For an easy-to-download version and further documentation of our dataset of aerial images of wind turbines, please visit our zenodo [link](https://zenodo.org/record/7385227#.Y419qezMLdr).

Each directory contains a README with further documentation. Overall, when it comes to:

**EXPERIMENTS:**
- Experiment results can be found in experiment_results
- Label and image paths as well as shape files for Yolov3 can be found in the experiments folder
- Yolov3 code for running our experiments can be found in the yolov3 folder, specifically the efficient_run_train_test.py script.
- Unless stated otherwise in a subdirectory README, experiment code can be reproduced in the environment found in requirements.txt.

**IMAGE GENERATION:**
- Code for our synthetic image generation technique is in image_generation/synthetic.
- Code for creating images of comparison techniques is in image_geration/comparison_techniques.

**DATASET:**
- The images and labels folders are symmetric and contain .jpg images and .txt labels of wind turbine locations.
- The domain_overview.json file is a map to the image and label folders and contains an overview of the image names by type and domain.
- NW, EM, and SW are common acronyms for Northwest, Eastern Midwest, and Southwest, which are the regions of the United States we gather turbines from.

If you use this repo or technique in an academic work, please cite:

@inproceedings{kornfein2022closing,
  title={Closing the Domain Gap -- Blended Synthetic Imagery for Climate Object Detection},
  author={Kornfein, Caleb and Willard, Frank and Tang, Caroline and Long, Yuxi and Jain, Saksham and Malof, Jordan and Ren, Simiao and Bradbury, Kyle},
  booktitle={NeurIPS 2022 Workshop on Tackling Climate Change with Machine Learning},
  url={https://www.climatechange.ai/papers/neurips2022/37},
  year={2022}
}

If you have any remaining questions, feel free to reach out at caleb.kornfein@gmail.com.
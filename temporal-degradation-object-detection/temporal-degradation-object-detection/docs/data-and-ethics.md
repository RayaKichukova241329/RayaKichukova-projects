# Data and ethics

A summary of the data management plan and ethics assessment written for the project.

## Datasets

| Period | Source | Licence | Images |
|---|---|---|---|
| 1982 to 1988 | New York City Municipal Archives, tax assessment photographs | Public domain, non-commercial research | 300 |
| 1998 | Getty Research Institute, Los Angeles street photography | Non-commercial academic research | about 150 |
| 1990s | London Picture Archive | Research use | about 150 |
| 2011 to 2012 | KITTI 2012, from KIT and the Toyota Technological Institute | Academic research | 300 |
| 2017+ | Mapillary Vistas | CC BY-SA 4.0 | 300 |

No primary data was collected. The Mapillary images were taken from a Kaggle competition dataset because of the size of the full dataset.

## Annotation and processing

I annotated all the 1980s and 1990s images from scratch in Roboflow, and the Building class for KITTI, which its original labels do not contain. Annotation took about two hours per 100 images and was reviewed visually after export. Processing steps: black borders removed from the 1980s images with the labels adjusted, Mapillary segmentation masks converted to bounding boxes with rider classes merged into Cyclist, KITTI labels converted to YOLO format with Van merged into Car, and all four datasets remapped to the five-class taxonomy.

## Privacy and GDPR

Street-level images can incidentally contain faces and number plates, which makes them personal data in principle. The risk was assessed per dataset: the New York collection was made for property tax assessment and generally shows no people, Mapillary blurs faces and plates before release, and KITTI was assessed by its authors. Processing falls under the research exemption of GDPR Article 89. No individual is identified, tracked or profiled, annotations describe object locations and classes only, and the images are not shared. The project was classified as low ethical risk and needed no formal approval.

## Bias

The historical images were sampled by hand from archives, which may favour images with clearly visible objects. The five classes reflect common urban detection benchmarks and encode no demographic characteristics.

## Why the data is not published

The source licences restrict redistribution. This repository contains the code and derived results only.

## AI tools

Claude (Anthropic) was used for code review and organisation, LaTeX formatting and document structure. NotebookLM (Google) was used for citation extraction. The research design, literature analysis, annotation decisions and conclusions are my own.

Back to the [project README](../README.md).

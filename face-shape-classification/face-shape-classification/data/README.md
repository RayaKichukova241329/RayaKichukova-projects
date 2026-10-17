# Dataset

The dataset is **not published**. It consists of photographs of real people, some of them public figures, collected from the web, and I do not have the right to redistribute them.

## Composition

| Class | Images |
|---|---|
| Heart | 195 |
| Round | 180 |
| Square | 189 |
| **Total** | **564** |

Images are 128 x 128 pixels in JPG format. The split is 80% training, 10% validation and 10% test.

## How it was built

1. Searched the web for each face shape and collected as many results as possible, plus a small number of generated images.
2. Removed images with sketched or drawn overlays on the face, and images that were not clearly frontal.
3. Converted all formats (PNG, JPEG, BMP, GIF, TIFF, WebP, AVIF) to JPG and skipped files that could not be opened.
4. Resized every image to 128 x 128, keeping the aspect ratio and padding the rest.
5. Checked that every image had the expected resolution and counted the images per class.

## Known limitations

- Collected from search results, so it reflects who appears in search results. For "round face shape" that was 80 Caucasian, 40 Asian and 26 African-American faces, and no Latino-American faces. See [`../docs/responsible-ai.md`](../docs/responsible-ai.md).
- Labels come from search terms, not from expert annotation, and many faces sit between two shapes.
- Small: a few hundred images per class.

## Expected layout for the notebook

```
Dataset_Images/
  Resized images_extra/
    Heart JPG/
    Round JPG/
    Square JPG/
```

To rebuild it, collect front-facing images you have the right to use and follow the steps above. A better route is a dataset with clear licences and consent, because of the privacy and copyright issues of scraped faces.

# LugandaLens

LugandaLens is a project for performing OCR (Optical Character Recognition) on Luganda language text images using TensorFlow.

## Installation

To install LugandaLens, you can use pip:

```bash
pip install lugandalens

Predicting on Batch of Images

You can use the following code to predict text from a batch of images:

python

from lugandalens import predict_batch_images

# Predict text from a folder containing images
image_folder = "path/to/your/image/folder"
output_file = "path/to/output/predictions.txt"
predict_batch_images(image_folder, output_file)

print("Predictions saved to:", output_file)

License

This project is licensed under the MIT License - see the LICENSE file for details.

kotlin


This updated README now reflects that the model loading is handled internally within the `lugandalens` package, and users only need to call the prediction functions provided by the package.



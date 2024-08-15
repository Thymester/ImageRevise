# ImageRevise

**ImageRevise** is a Python application built with Tkinter and PIL (Pillow) for resizing and watermarking images. It provides a user-friendly GUI for processing images and offers various features like maintaining aspect ratio, adding watermarks, and optimizing image quality.

## Features

- **Resize Images**: Adjust the size of images while maintaining or not maintaining the aspect ratio.
- **Add Watermarks**: Add custom watermarks to images with adjustable size and position.
- **Optimize Images**: Compress images for web use by adjusting quality settings.
- **Remove Metadata**: Optionally remove EXIF metadata from images.
- **Preview Images**: View a preview of the resized and watermarked image before saving.
- **View Metadata**: Display EXIF metadata of the selected image.
- **AND MORE**: View releases to see everything this app offers.

## Requirements

- Python 3.x
- Pillow library (`PIL`)
- Tkinter (usually included with Python)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Thymester/imagerevise.git
    ```

2. Navigate to the project directory:

    ```bash
    cd imagerevise
    ```

3. Install the required Python packages:

    ```bash
    pip install pillow
    pip install tk
    ```

## Usage

1. Run the application:

    ```bash
    python imagerevise.py
    ```

2. Use the GUI to:
    - **Browse**: Select an image file, output directory, and watermark image.
    - **Set Options**: Choose the image size, watermark position, and format. Adjust quality and metadata settings.
    - **Process Images**: Click "Process Images" to resize, watermark, and optimize your image.
    - **Preview Image**: Click "Preview Image" to see a rough preview of the processed image.
    - **View Metadata**: Click "View Metadata" to check the EXIF metadata of the selected image.

## GUI Layout

- **Input Image**: Text entry and browse button to select the image file.
- **Output Directory**: Text entry and browse button to select the output directory.
- **Watermark Image**: Text entry and browse button to select the watermark image.
- **Watermark Size**: Input fields for setting the watermark width and height.
- **Watermark Position**: Dropdown menu to select the position of the watermark.
- **Size**: Dropdown menu to choose preset sizes or enter custom dimensions.
- **Format**: Dropdown menu to select the output image format (JPEG or PNG).
- **Quality**: Slider to adjust the image quality.
- **Keep Aspect Ratio**: Checkbox to maintain the original aspect ratio of the image.
- **Keep Metadata**: Checkbox to retain or remove metadata.

## Example

Here's an example of how to resize an image and add a watermark:

1. Select an input image and an output directory.
2. Choose a watermark image and set its size and position.
3. Select the desired output size and format.
4. Click "Process Images" to start the processing.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to open issues or submit pull requests to contribute to this project. Contributions are welcome!

## Acknowledgements

- **Pillow** for image processing.
- **Tkinter** for the graphical user interface.

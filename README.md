# ImageRevise

**ImageRevise** is a simple Tkinter-based application for resizing and optimizing images. It allows users to add watermarks, resize images while maintaining aspect ratio, and optimize them for web use. Additionally, it provides functionality to view and remove EXIF metadata from images.

## Features

- Resize images while maintaining aspect ratio.
- Custom Resize while maintaining aspect ratio.
- Add watermarks to images with adjustable positions.
- Optimize images for web use by adjusting quality.
- Remove EXIF metadata from images.
- View EXIF metadata in your images.
- Preview images before saving.
- Browse and select input files, output directories, and watermark images using file dialogs.
- **AND MORE**
  
[View releases](https://github.com/Thymester/ImageRevise/releases) for more information!

## Requirements

- Python 3.x
- Pillow library (`PIL`)
- Tkinter library (included with Python)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Thymester/imagerevise.git
    ```

2. Navigate to the project directory:

    ```bash
    cd image-revise
    ```

3. Install required Python packages:

    ```bash
    pip install pillow
    ```

## Usage

1. Run the application:

    ```bash
    python image_revise.py
    ```

2. In the GUI:
    - **Input Image:** Click "Browse" to select the image you want to process.
    - **Output Directory:** Click "Browse" to select the directory where processed images will be saved.
    - **Watermark Image:** Click "Browse" to select a watermark image.
    - **Select Size:** Choose the desired size (Small, Medium, Large) for resizing the image.
    - **Select Format:** Choose the image format (JPEG or PNG).
    - **Select Quality:** Adjust the quality level for JPEG images (1-100).
    - **Keep Aspect Ratio:** Check or uncheck to maintain the original aspect ratio.
    - **Remove Metadata:** Check to remove EXIF metadata from the processed image.
    - **Watermark Position:** Select the position for the watermark (center, bottom_right, bottom_left, top_right, top_left).
    - **Process Images:** Click to resize, add watermark, and optimize the image.
    - **View Metadata:** Click to view EXIF metadata of the selected image.
    - **Preview:** A preview of the resized image with the watermark will be displayed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork the repository and submit pull requests. For bug reports or feature requests, please use the [Issues](https://github.com/Thymester/imagerevise/issues) page.

## Acknowledgements

- Pillow library for image processing.
- Tkinter library for creating the GUI.

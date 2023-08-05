## Image Deduplication and Organization Tool

This tool is designed to download images from an Excel file, organize them in separate folders, and then perform image deduplication based on Structural Similarity Index (SSIM).

### Prerequisites
 - Python 3.6+
 - TensorFlow
 - pandas
 - requests
 - concurrent.futures

## Installation
1. Clone this repository to your local machine.
2. Install the required Python packages using pip:
```commandline
pip install -r requirements.txt
```

### Usage
1. Place the **main.py**, **find_SSIM.py**, and ***.xlsx** file in the same directory.
2. Run the **main.py** script:
```python
python main.py
```

### **compare-images-directly.py**
This script is used when you already have images in respective folders and just want to perform image-de-duplication. It then calls the search_duplicate_images function from find_SSIM.py to perform image deduplication.

### Instructions
1. Replace the placeholder './Image_Searching.xlsx' in the script with the actual file path of your Excel file.
2. When prompted, enter the sheet names for the "To_Find" and "Master_Data" DataFrames. If the sheet names are not provided, the default names "To_Find" and "Master_Data" will be used.

### Note
Adjust the similarity_threshold in the search_duplicate_images function according to your requirement. A lower value will be more stringent, and a higher value will be more lenient in detecting duplicates.


import os
import pandas as pd
import requests
import concurrent.futures

from find_SSIM import search_duplicate_images


# Function to download an image from URL and save it with a specific filename
def download_image(url, filename):
    res = requests.get(url)
    if res.status_code != 200:
        return "Image Not Found"
    with open(filename, 'wb') as f:
        f.write(res.content)
    return "OK"


# Function to create a folder if it doesn't exist
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def download_images_for_df(df, folder, item_code_column, image_url_column):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        # Download images and save them in the respective folders
        for index, row in df.iterrows():
            item_code = str(row[item_code_column])
            item_color = str(row['Color']).replace('/', '-')
            image_url = str(row[image_url_column])
            image_filename = f'{folder}/{item_code}-{item_color}.jpg'
            print(f"Downloading {image_url} ...")
            futures.append(executor.submit(download_image, image_url, image_filename))

        for future, index, row in zip(concurrent.futures.as_completed(futures), df.index, df.itertuples()):
            item_code = str(row[1])
            item_color = str(row[2]).replace('/', '-')
            image_filename = f'{folder}/{item_code}-{item_color}.jpg'
            response = future.result()
            if response != "OK":
                print(f"*ERROR* ::: Image-{image_url} Not Found.\n")
            else:
                print(f"Image-{image_filename} ::: Color-{item_color} Downloaded Successfully.")


try:
    # Read the Excel file and its sheets
    file_path = './Image_Searching.xlsx'  # Replace this with the actual file path
    to_find_sheet = input("Enter To-Find Sheet Name from Excel File: ") or "To_Find"
    master_data_sheet = input('Enter Master-Data Sheet Name from Excel File: ') or "Master_Data"

    df_to_find = pd.read_excel(file_path, sheet_name=to_find_sheet)
    df_master_data = pd.read_excel(file_path, sheet_name=master_data_sheet)

    # Create folders for "To_Find" and "Master_Data"
    create_folder('To_Find')
    create_folder('Master_Data')

    # Call the function to download images for both dataframes in parallel
    download_images_for_df(df_to_find, to_find_sheet, 'Shopify ID', 'To Find')
    download_images_for_df(df_master_data, master_data_sheet, 'Item Code', 'Image URl')

    print("#" * 100)
    print("Completed Image downloading and Organizing.")
    print("#" * 100)
    print("#" * 100)
    print("Starting with Image De-Duplication processing ...")
    print("#" * 100)

    search_duplicate_images("./To_Find", "./Master_Data")

except (FileNotFoundError, ValueError) as err:
    print(f"An Error Occurred ::: {err}")

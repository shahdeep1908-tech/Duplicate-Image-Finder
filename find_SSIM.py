import os
import tensorflow as tf
import numpy as np


def preprocess_image(image_path):
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = tf.keras.applications.resnet50.preprocess_input(image)
    return image


def compute_image_embedding(image_path, model):
    image = preprocess_image(image_path)
    batch = np.expand_dims(image, axis=0)
    return model.predict(batch).flatten()


def find_similar_images(folder1, folder2, similarity_threshold=0.7):
    model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, pooling='avg')

    similar_pairs = []
    folder1_embeddings = {}

    # Process images in folder 1 and compute embeddings
    for filename1 in os.listdir(folder1):
        if filename1.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
            image1_path = os.path.join(folder1, filename1)
            folder1_embeddings[filename1] = compute_image_embedding(image1_path, model)

    # Compare images in folder 2 with images in folder 1
    for filename2 in os.listdir(folder2):
        if filename2.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
            image2_path = os.path.join(folder2, filename2)
            print(image2_path)
            embedding2 = compute_image_embedding(image2_path, model)

            for filename1, embedding1 in folder1_embeddings.items():
                similarity_score = np.dot(embedding1, embedding2) / (
                        np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
                if similarity_score >= similarity_threshold:
                    similar_pairs.append((os.path.join(folder1, filename1), image2_path))

    return similar_pairs


def search_duplicate_images(folder1_path, folder2_path):
    similarity_threshold = 0.7  # Adjust this threshold as per your requirement

    if similar_images := find_similar_images(folder1_path, folder2_path, similarity_threshold):
        print("Similar images found:")
        for image1, image2 in similar_images:
            print(f"Folder 1: {image1}, Folder 2: {image2}")
    else:
        print("No similar images found.")

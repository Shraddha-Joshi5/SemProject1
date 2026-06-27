import torch
#import psycopg2
import numpy as np
#import uuid
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1

mtcnn = MTCNN(image_size=160, margin=20, keep_all=False)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

def get_embedding(image_path: str) -> np.ndarray:
    img = Image.open(image_path).convert('RGB')
    face_tensor = mtcnn(img)
    if face_tensor is None:
        raise ValueError("No face detected in image")
    with torch.no_grad():
        embedding = resnet(face_tensor.unsqueeze(0))
    embedding = embedding.squeeze().numpy()
    embedding = embedding / np.linalg.norm(embedding)
    return embedding

# test_embedding.py
from enroll_face import get_embedding
import numpy as np

# Test 1: Valid image
embedding = get_embedding("t1.jpg")
print("Shape:", embedding.shape)          # Should be (512,)
print("Norm:", np.linalg.norm(embedding)) # Should be ~1.0

#Test_2
def cosine_similarity(a, b):
    return np.dot(a, b)  # already normalized, so dot = cosine

emb1 = get_embedding("t1.jpg")
emb2 = get_embedding("t3.jpg")  # different photo, same person
emb3 = get_embedding("t2.jpg")     # different person

print("Same person score:", cosine_similarity(emb1, emb2))  # expect > 0.7
print("Diff person score:", cosine_similarity(emb1, emb3))  # expect < 0.5
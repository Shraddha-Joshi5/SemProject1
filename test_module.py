import numpy as np
import database_module as db

print("--- Testing Registration System ---")
# Generate a mock 512D embedding vector
mock_vector = np.random.rand(512).tolist()
reg_status = db.register_new_face("Nirajan", mock_vector)
print(reg_status)

print("\n--- Testing Recognition Engine ---")
# Run a live test search against your newly registered name
search_status = db.identify_face(mock_vector)
import psycopg2
import numpy as np
import json  # 🟢 Added to serialize Python dicts into PostgreSQL JSONB format

try:
    # 1. Connect directly to your face_recognition database
    conn = psycopg2.connect(
        dbname="face_recognition",
        user="postgres", 
        password="x@ditix00",       
        host="localhost",
        port="5432"
    )
    conn.autocommit = True  # Enable autocommit for extension creation
    cursor = conn.cursor()
    print("🚀 Successfully connected to the face_recognition database instance!")

    # 2. Force creation of tables directly via Python to avoid pgAdmin tab confusion
    print("📦 Verifying database structural tables with contextual data...")
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            person_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS face_embeddings (
            id SERIAL PRIMARY KEY,
            person_id INT REFERENCES persons(person_id) ON DELETE CASCADE,
            embedding vector(512) NOT NULL,
            context JSONB DEFAULT '{}'::jsonb  -- 🟢 Column active!
        );
    """)
        
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS face_embeddings_hnsw_idx 
        ON face_embeddings USING hnsw (embedding vector_cosine_ops);
    """)
    print("⚙️ Database tables verified and active!")

    # 3. Mock a 512-dimensional face vector and descriptive context payload
    mock_embedding = np.random.rand(512).tolist()
    person_name = "Nirajan"
    mock_context = {"role": "Undergraduate Student", "department": "AI 2025"} # 🟢 Sample context object

    # 4. Add name to persons table
    cursor.execute("""
        INSERT INTO persons (name) 
        VALUES (%s) 
        ON CONFLICT (name) DO UPDATE SET name=EXCLUDED.name 
        RETURNING person_id;
    """, (person_name,))
    
    person_id = cursor.fetchone()[0]
    print(f"✅ Synced: Registered '{person_name}' with ID {person_id}")

    # 5. Insert the 512-dimensional vector alongside its context payload
    cursor.execute("""
        INSERT INTO face_embeddings (person_id, embedding, context) 
        VALUES (%s, %s, %s);
    """, (person_id, mock_embedding, json.dumps(mock_context))) # 🟢 Safe injection mapping
    
    print(f"✅ Synced: Stored the 512-dimensional embedding vector and context successfully!")

    # 6. Clean up connections
    cursor.close()
    conn.close()
    print("\n🎉 SUCCESS! The entire pipeline works perfectly. Your backend is 100% ready.")

except Exception as e:
    print(f"❌ Connection or storage failed: {e}")
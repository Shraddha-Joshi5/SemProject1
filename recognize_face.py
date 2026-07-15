import psycopg2
import numpy as np

def get_db_connection():
    """Manages the connection to your local face_recognition database."""
    return psycopg2.connect(
        dbname="face_recognition",
        user="postgres", 
        password="x@ditix00",       
        host="localhost",
        port="5432"
    )

def identify_face(live_embedding, threshold=0.4):
    """Compares a live 512D camera vector against stored vectors using HNSW Cosine Distance."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        
        query = """
            SELECT 
                p.name, 
                (f.embedding <=> %s::vector) AS distance,
                COALESCE(f.context::text, '{}') AS context
            FROM public.face_embeddings f
            JOIN public.persons p ON f.person_id = p.person_id
            ORDER BY distance ASC
            LIMIT 1;
        """
        
        cursor.execute(query, (live_embedding,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if result:
            name, distance, context = result
           
            if distance < threshold:
                return f" Match: {name} (Distance: {distance:.4f}) | Context: {context}"
            else:
                return f" Unknown Person (Closest guess: {name} with distance {distance:.4f})"
        else:
            return " Database is currently empty."

    except Exception as e:
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query_fallback = """
                SELECT p.name, (f.embedding <=> %s::vector) AS distance
                FROM public.face_embeddings f
                JOIN public.persons p ON f.person_id = p.person_id
                ORDER BY distance ASC
                LIMIT 1;
            """
            cursor.execute(query_fallback, (live_embedding,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result:
                name, distance = result
                if distance < threshold:
                    return f" Match: {name} (Distance: {distance:.4f}) | No speech context registered."
                return f" Unknown Person (Closest guess: {name} with distance {distance:.4f})"
            return " Database is currently empty."
        except Exception as fallback_error:
            return f" Database Query Error: {fallback_error}"

# --
if __name__ == "__main__":
    print(" Simulating a live camera vector search against 'face_recognition'...")
    
    test_camera_vector = np.random.uniform(-0.1, 0.1, 512).tolist()
    
    match_result = identify_face(test_camera_vector)
    print(match_result)
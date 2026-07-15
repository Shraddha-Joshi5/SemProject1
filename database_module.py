import json
import psycopg2

def get_db_connection():
    """Manages connection details dynamically for the Docker network environment."""
    # When running on your local machine outside of the Docker network, 
    # you might need host="localhost". If running inside Docker, keep host="postgres".
    try:
        return psycopg2.connect(
            dbname="facedb",        
            user="user",            
            password="password",    
            port="5432"
        )
    except psycopg2.OperationalError:
        
        return psycopg2.connect(
            dbname="facedb",
            user="user",
            password="password",
            host="postgres",
            port="5432"
        )

def register_new_face(name, raw_512d_vector, context=None):
    """
    Inserts a new identity, their 512D face vector, and optional metadata 
    context (such as audio transcriptions) into the database.
    """
    if context is None:
        context = {}

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        
        cursor.execute(
            "INSERT INTO public.persons (name) VALUES (%s) RETURNING person_id;", 
            (name,)
        )
        person_id = cursor.fetchone()[0]

        
        cursor.execute(
            """
            INSERT INTO public.face_embeddings (person_id, embedding, context) 
            VALUES (%s, %s::vector, %s);
            """,
            (person_id, raw_512d_vector, json.dumps(context))
        )

        conn.commit()
        cursor.close()
        conn.close()
        return f" Successfully registered {name} (ID: {person_id})"
    except Exception as e:
        return f" Registration Error: {e}"

def identify_face(live_embedding, threshold=0.4):
    """Compares a live 512D camera vector against stored vectors using HNSW Cosine Distance."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        
        query = """
            SELECT p.name, (f.embedding <=> %s::vector) AS distance, f.context
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
        return f" Database Query Error: {e}"
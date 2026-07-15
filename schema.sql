
CREATE EXTENSION IF NOT EXISTS vector;


DROP TABLE IF EXISTS public.face_embeddings CASCADE;
DROP TABLE IF EXISTS public.persons CASCADE;


CREATE TABLE public.persons (
    person_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE public.face_embeddings (
    embedding_id SERIAL PRIMARY KEY,
    person_id INT REFERENCES public.persons(person_id) ON DELETE CASCADE,
    embedding vector(512) NOT NULL,
    context JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS face_embeddings_hnsw_idx 
ON public.face_embeddings USING hnsw (embedding vector_cosine_ops);
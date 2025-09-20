import psycopg2
import psycopg2._psycopg
import psycopg2.extras
import common.llmclient

class SkillFinder:
    def __init__(self, conn: psycopg2._psycopg.connection):
        self.embedder = common.llmclient.LLMEmbedder()
        self.conn = conn
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id, name, embeddings FROM skills")
            skills = cur.fetchall()
            skill_ids, embeddings = [], []
            if any(skill['embeddings'] == None for skill in skills):
                skill_ids = [i['id'] for i in skills]
                embeddings = self.embedder.embed([i['name'] for i in skills]).data
                embeddings = [i.embedding for i in embeddings]
                cur.executemany('UPDATE skills SET embeddings = %s WHERE id = %s', zip(embeddings, skill_ids))

    def normalize_skills(self, skills: dict[str, int]):
        embeddings = self.embedder.embed(skills.keys())
        embeddings = [i.embedding for i in embeddings.data]
        ids_to_vals = {}
        with self.conn.cursor() as cur:
            for skill_name, embedding in zip(skills, embeddings):
                cur.execute("""
                    SELECT id
                    FROM skills
                    ORDER BY embeddings <-> (%s::vector)
                    LIMIT 1;
                """, (embedding,))
                fetched = cur.fetchone()
                skill_id = fetched[0]
                ids_to_vals[skill_id] = skills[skill_name]

        return ids_to_vals
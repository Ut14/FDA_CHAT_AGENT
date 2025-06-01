import aiomysql
import os

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "12345"),
    "db": os.getenv("MYSQL_DB", "fda")
}

async def get_connection():
    return await aiomysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        db=DB_CONFIG["db"]
    )

async def search_adverse_event_by_date(start_date: str, end_date: str) -> str:
    query = """
    SELECT COUNT(*), GROUP_CONCAT(DISTINCT drug_name SEPARATOR ', ') FROM fda_reports
    WHERE receivedate BETWEEN %s AND %s
    """
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, (start_date, end_date))
            result = await cur.fetchone()
    count = result[0]
    drugs = result[1] or ""
    if count == 0:
        return f"No reports found between {start_date} and {end_date}."
    return f"🗂️ {count} reports found from {start_date} to {end_date}.\nReported drugs: {drugs[:500]}..."

async def search_drug_by_pharmacologic_class(pharm_class: str) -> str:
    query = """
    SELECT drug_name, COUNT(*) as count FROM fda_reports
    WHERE drug_name LIKE %s
    GROUP BY drug_name
    ORDER BY count DESC
    LIMIT 10
    """
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, (f"%{pharm_class}%",))
            rows = await cur.fetchall()
    if not rows:
        return f"No drugs found in pharmacologic class '{pharm_class}'."
    return "\n".join([f"{drug} – {count} reports" for drug, count in rows])

async def count_patient_reactions(pharm_class: str) -> str:
    query = """
    SELECT reaction, COUNT(*) as count FROM fda_reports
    WHERE drug_name LIKE %s
    GROUP BY reaction
    ORDER BY count DESC
    LIMIT 10
    """
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, (f"%{pharm_class}%",))
            rows = await cur.fetchall()
    if not rows:
        return f"No reactions found for class '{pharm_class}'."
    return "\n".join([f"{reaction} – {count}" for reaction, count in rows])

async def search_drug_by_name(drug_name: str) -> str:
    query = """
    SELECT reaction, COUNT(*) as count FROM fda_reports
    WHERE drug_name LIKE %s
    GROUP BY reaction
    ORDER BY count DESC
    LIMIT 10
    """
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, (f"%{drug_name}%",))
            rows = await cur.fetchall()
    if not rows:
        return f"No adverse effects found for drug '{drug_name}'."
    return "\n".join([f"{reaction} – {count} reports" for reaction, count in rows])

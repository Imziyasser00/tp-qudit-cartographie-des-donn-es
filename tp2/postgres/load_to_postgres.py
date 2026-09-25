import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

CONN_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "dbname": "football_international",
    "user": "postgres",
    "password": "2001",
}

CLEAN_FILE = "../datalake/clean/matches_clean.csv"


def get_or_create_equipe(cur, cache, nom):
    if nom in cache:
        return cache[nom]
    cur.execute("SELECT id_equipe FROM equipe WHERE nom = %s", (nom,))
    row = cur.fetchone()
    if row:
        cache[nom] = row[0]
        return row[0]
    cur.execute("INSERT INTO equipe (nom) VALUES (%s) RETURNING id_equipe", (nom,))
    new_id = cur.fetchone()[0]
    cache[nom] = new_id
    return new_id


def get_or_create_tournoi(cur, cache, nom):
    if nom in cache:
        return cache[nom]
    cur.execute("SELECT id_tournoi FROM tournoi WHERE nom = %s", (nom,))
    row = cur.fetchone()
    if row:
        cache[nom] = row[0]
        return row[0]
    cur.execute("INSERT INTO tournoi (nom) VALUES (%s) RETURNING id_tournoi", (nom,))
    new_id = cur.fetchone()[0]
    cache[nom] = new_id
    return new_id


def run():
    df = pd.read_csv(CLEAN_FILE)
    print(f"Lignes à charger : {len(df)}")

    conn = psycopg2.connect(**CONN_PARAMS)
    cur = conn.cursor()

    equipe_cache = {}
    tournoi_cache = {}
    inserted, skipped = 0, 0

    for i, row in df.iterrows():
        try:
            id_dom = get_or_create_equipe(cur, equipe_cache, row["equipe_domicile"])
            id_ext = get_or_create_equipe(cur, equipe_cache, row["equipe_exterieur"])
            if id_dom == id_ext:
                skipped += 1
                continue
            id_tournoi = get_or_create_tournoi(cur, tournoi_cache, row["competition"])

            score_dom = None if pd.isna(row["score_domicile"]) else int(row["score_domicile"])
            score_ext = None if pd.isna(row["score_exterieur"]) else int(row["score_exterieur"])
            ville = None if pd.isna(row["ville"]) else row["ville"]
            id_externe = None if pd.isna(row["id_externe"]) else int(row["id_externe"])

            if row["source"] == "api_live" and id_externe is not None:
                                cur.execute("""
                    INSERT INTO match (date_match, id_equipe_domicile, id_equipe_exterieur,
                        score_domicile, score_exterieur, id_tournoi, ville, pays,
                        terrain_neutre, source, id_externe, statut)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (date_match, id_equipe_domicile, id_equipe_exterieur, source)
                    DO NOTHING
                """, (row["date_match"], id_dom, id_ext, score_dom, score_ext,
                      id_tournoi, ville, row["pays"], False, row["source"],
                      id_externe, row["statut"]))
            else:
                cur.execute("""
                    INSERT INTO match (date_match, id_equipe_domicile, id_equipe_exterieur,
                        score_domicile, score_exterieur, id_tournoi, ville, pays,
                        terrain_neutre, source, id_externe, statut)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (date_match, id_equipe_domicile, id_equipe_exterieur, source)
                    DO NOTHING
                """, (row["date_match"], id_dom, id_ext, score_dom, score_ext,
                      id_tournoi, ville, row["pays"], False, row["source"],
                      id_externe, row["statut"]))
            inserted += 1
        except Exception as e:
            print(f"Erreur ligne {i} : {e}")
            conn.rollback()
            skipped += 1
            continue

        if inserted % 2000 == 0:
            conn.commit()
            print(f"{inserted} lignes insérées...")

    conn.commit()
    print(f"Terminé. Insérées : {inserted}, ignorées : {skipped}")
    cur.close()
    conn.close()


if __name__ == "__main__":
    run()
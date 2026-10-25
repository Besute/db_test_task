from ..auxiliary.auxiliary_functions import read_json
from ..auxiliary.constants import PROJ

def create_tables(database):
    """
        Создание архитектуры: создаются таблицы и записываются данные из json
    """
    connection = database.connect()
    with connection as c:
        with c.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS versions (id SERIAL PRIMARY KEY, vendor TEXT, product TEXT, version TEXT);")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS vulnerabilities (id SERIAL PRIMARY KEY, vendor TEXT, "
                "product TEXT, KLA_id TEXT, description TEXT, "
                "publish_date DATE, start_vuln_version TEXT, fixed_version TEXT);"
            )
            versions = read_json(PROJ / "data" / "versions.json")
            vulnerabilities = read_json(PROJ / "data" / "vulnerabilities.json")
            cur.execute(f"TRUNCATE versions;")
            cur.execute(f"TRUNCATE vulnerabilities;")
            for version in versions:
                cur.execute(
                    f"INSERT INTO versions (vendor, product, version)  VALUES ('{version["vendor"]}', '{version["product"]}', '{version["version"]}')")

            for vulnerability in vulnerabilities:
                cur.execute(f"INSERT INTO vulnerabilities (vendor, product, KLA_id, description, "
                            f"publish_date, start_vuln_version, fixed_version)"
                            f"VALUES ('{vulnerability["vendor"]}', '{vulnerability["product"]}', "
                            f"'{vulnerability["KLA_id"]}', '{vulnerability["description"]}', "
                            f"'{vulnerability["publish_date"]}', '{vulnerability["start_vuln_version"]}', "
                            f"'{vulnerability["fixed_version"]}');")
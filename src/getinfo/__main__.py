from .db.db import DB
import argparse
import os
from dotenv import load_dotenv
from pathlib import Path
from .auxiliary.auxiliary_functions import read_json

PROJ = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJ / ".env", override=True)


def build_parser():
    """
    Создаёт парсер для командной строки

    Здесь 2 параметра: --product и --version для названия продукта и указания версии соотвественно
    """
    parser = argparse.ArgumentParser(prog="getinfo")

    parser.add_argument("--product", required=True, help="Name of the product")
    parser.add_argument("--version", default=None, help="Version of the product")

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    database = DB(os.environ["DB_NAME"], os.environ["DB_USER"], os.environ["DB_PASSWORD"], os.environ["DB_HOST"], os.environ["DB_PORT"])
    connection = database.connect()
    with connection as c:
        with c.cursor() as cur:
            """
                Создание архитектуры: создаются таблицы и записываются данные из json
            """
            cur.execute("CREATE TABLE IF NOT EXISTS versions (id SERIAL PRIMARY KEY, vendor TEXT, product TEXT, version TEXT);")
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
                cur.execute(f"INSERT INTO versions (vendor, product, version)  VALUES ('{version["vendor"]}', '{version["product"]}', '{version["version"]}')")

            for vulnerability in vulnerabilities:
                cur.execute(f"INSERT INTO vulnerabilities (vendor, product, KLA_id, description, "
                            f"publish_date, start_vuln_version, fixed_version)"
                            f"VALUES ('{vulnerability["vendor"]}', '{vulnerability["product"]}', "
                            f"'{vulnerability["KLA_id"]}', '{vulnerability["description"]}', "
                            f"'{vulnerability["publish_date"]}', '{vulnerability["start_vuln_version"]}', "
                            f"'{vulnerability["fixed_version"]}');")

if __name__ == '__main__':
    """
        ПЕРЕД ЗАПУСКОМ ПРОЧТИТЕ README
    """
    main()
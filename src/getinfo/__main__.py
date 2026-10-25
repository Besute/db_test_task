from .db.db import DB
import os
from dotenv import load_dotenv
from pathlib import Path
from .auxiliary.auxiliary_functions import read_json
from .auxiliary.auxiliary_functions import make_list_equal
from .auxiliary.auxiliary_functions import build_parser
from .Errors.errors import FailedConnectionErrors

PROJ = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJ / ".env", override=True)


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

def expression(good, checking, vuln):
    """
    Здесь идёт проверка на то, является ли нынешняя версия с ошибкой.
    good - версия без ошибкт
    checking - проверяемая версия
    vuln - версия, начиная с которой ошибка
    """

    for i in range(len(vuln)):
        if vuln[i] > checking[i]:
            return True
        elif vuln[i] < checking[i]:
            break

    is_fixed = True
    for i in range(len(good)):
        if good[i] > checking[i]:
            is_fixed = False
            break
        elif good[i] < checking[i]:
            break
    return is_fixed

def find_no_vuls(database, args):
    connection = database.connect()
    good_versions = []
    with connection as c:
        with c.cursor() as cur:
            cur.execute(
                f"SELECT start_vuln_version, fixed_version FROM vulnerabilities WHERE product = '{args.product}';")
            res_of_vuln = cur.fetchall()
            cur.execute(f"SELECT version FROM versions WHERE product = '{args.product}';")
            res_of_vers = cur.fetchall()
            for version in res_of_vers:
                version_by_dots = list(map(int, version[0].split(".")))
                bool_ok = True
                for vulnerability in res_of_vuln:
                    vuln = [int(vulnerability[0])]
                    good_by_dots = list(map(int, vulnerability[1].split(".")))

                    # Здесь я делаю все списки равными по длине для удобного сравнения
                    version_by_dots, good_by_dots = make_list_equal(version_by_dots, good_by_dots)
                    vuln, good_by_dots = make_list_equal(vuln, good_by_dots)

                    bool_ok = expression(good_by_dots, version_by_dots, vuln)
                    if not bool_ok:
                        break

                if bool_ok:
                    good_versions.append(version[0])
                    break
    return good_versions

def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        database = DB(os.environ["DB_NAME"], os.environ["DB_USER"], os.environ["DB_PASSWORD"], os.environ["DB_HOST"], os.environ["DB_PORT"])
        create_tables(database)
    except Exception as e:
        raise FailedConnectionErrors(f"Ошибка в подключении к базе данных. Пожалуйста, прочтите README и настройте окружение. Полная ошибка: {e}")

    if args.version is None:
        res = find_no_vuls(database, args)

if __name__ == '__main__':
    """
        ПЕРЕД ЗАПУСКОМ ПРОЧТИТЕ README
    """
    try:
        main()
    except Exception as e:
        print("Проишошла ошибка!", e)

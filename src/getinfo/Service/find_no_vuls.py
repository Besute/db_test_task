from ..auxiliary.auxiliary_functions import make_list_equal

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
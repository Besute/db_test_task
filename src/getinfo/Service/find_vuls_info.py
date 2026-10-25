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

def find_vuls_info(database, args):
    connection = database.connect()
    version_by_dots = list(map(int, args.version.split(".")))
    info = []
    with connection as c:
        with c.cursor() as cur:
            cur.execute(
                f"SELECT * FROM vulnerabilities WHERE product = '{args.product}';")
            res_of_vuln = cur.fetchall()
            for vulnerability in res_of_vuln:
                vuln = [int(vulnerability[-2])]
                good_by_dots = list(map(int, vulnerability[-1].split(".")))

                version_by_dots, good_by_dots = make_list_equal(version_by_dots, good_by_dots)
                vuln, good_by_dots = make_list_equal(vuln, good_by_dots)

                is_good = expression(good_by_dots, version_by_dots, vuln)
                if not is_good:
                    info.append(vulnerability[:-2])
    return info
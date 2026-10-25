from .db.db import DB
import os
from dotenv import load_dotenv
from .auxiliary.auxiliary_functions import build_parser
from .Errors.errors import FailedConnectionErrors
from .db.tables_creation import create_tables
from .Service.find_no_vuls import find_no_vuls
from .auxiliary.constants import PROJ

load_dotenv(PROJ / ".env", override=True)

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
        print(*res)

if __name__ == '__main__':
    """
        ПЕРЕД ЗАПУСКОМ ПРОЧТИТЕ README
    """
    try:
        main()
    except Exception as e:
        print("Проишошла ошибка!", e)

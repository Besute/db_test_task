from .db.db import DB
import argparse
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent.parent
ENV = PROJ.joinpath(".env")
load_dotenv(ENV, override=True)


def build_parser():
    parser = argparse.ArgumentParser(prog="getinfo")

    parser.add_argument("--product", required=True, help="Name of the product")
    parser.add_argument("--version", default=None, help="Version of the product")

    return parser

async def main():
    parser = build_parser()
    args = parser.parse_args()
    database = DB(os.environ["DB_NAME"], os.environ["DB_USER"], os.environ["DB_PASSWORD"], os.environ["DB_HOST"], os.environ["DB_PORT"])
    connection = database.connect()
    with connection as c:
        with c.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS versions (vendor TEXT, product TEXT, version TEXT)")
            cur.execute("CREATE TABLE IF NOT EXISTS vulnerabilities (vendor TEXT, product TEXT, KLA_id TEXT, "
                        "description TEXT, publish_date DATE, start_vuln_version TEXT, "
                        "fixed_version TEXT)")
    if args.version is None:
        pass
if __name__ == '__main__':
    asyncio.run(main())
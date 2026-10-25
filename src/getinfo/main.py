from .db.db import DB
import argparse
import asyncio

def build_parser():
    parser = argparse.ArgumentParser(prog="getinfo")

    parser.add_argument("--product", required=True, help="Name of the product")
    parser.add_argument("--version", default=None, help="Version of the product")

    return parser

async def main():
    parser = build_parser()
    args = parser.parse_args()
    database = DB("db_getinfo", "boris", "MoZaIcHnIy1!", "localhost", 5432)
    connection = await database.connect()
    with connection as c:
        with c.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS versions (vendor TEXT, product TEXT, version TEXT)")
            cur.execute("CREATE TABLE IF NOT EXISTS vulnerabilities (vendor TEXT, product TEXT, KLA_id TEXT, "
                        "description TEXT, publish_date DATE, start_vuln_version INTEGER, end_vuln_version INTEGER, "
                        "fixed_version TEXT)")
    if args.version is None:
        pass

if __name__ == '__main__':
    asyncio.run(main())
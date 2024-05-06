import aiosqlite
import asyncio
import logging
import os
import rich_click as click
from rich.console import Console

import snapcat.config as Config

log = logging.getLogger("snapcat")
console = Console()


async def get_cat_db_info(db):
    async with db.execute("SELECT count(*) FROM coin_spends") as cursor:
        row = await cursor.fetchone()
        spend_count = row[0]
    async with db.execute("SELECT count(*) FROM coins") as cursor:
        row = await cursor.fetchone()
        coins_count = row[0]

    async with db.execute(
        "SELECT value FROM config WHERE key = 'last_block_height'"
    ) as cursor:
        row = await cursor.fetchone()
        last_block_height = None if row is None else int(row[0])

    return spend_count, coins_count, last_block_height


@click.command(help="Display the CAT db information.")
@click.pass_context
def show(ctx):
    async def _show():
        db_file_name = ctx.obj["db_file_name"]
        if db_file_name is None:
            message = "No database file name provided"
            log.error(message)
            console.print(f"[bold red]{message}")
            exit()

        db_file = f"{Config.database_path}/{db_file_name}"
        if not os.path.exists(db_file):
            message = "No database file found, please sync first"
            log.error(message)
            console.print(f"[bold red]{message}")
            exit()

        async with aiosqlite.connect(db_file_name) as db:
            async with db.execute(
                "SELECT value FROM config WHERE key = 'tail_hash'"
            ) as cursor:
                row = await cursor.fetchone()
                tail_hash = None if row is None else row[0]
                if tail_hash is None:
                    message = "No tail hash found, please sync first"
                    log.error(message)
                    console.print(f"[bold red]{message}")
                    exit()
            log.info(f"Exporting CAT holders for {tail_hash}")
            spend_count, coins_count, last_block_height = await get_cat_db_info(db)

            console.print(f"Tail Hash: [bold bright_cyan]{tail_hash}")
            console.print(f"# of Coins Spent: {spend_count}")
            console.print(f"# of Coins Created: {coins_count}")
            console.print(f"Last Block Height: {last_block_height}")

    asyncio.run(_show())

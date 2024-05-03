import shutil

from loguru import logger

from odoo_openupgrade_wizard.tools.tools_postgres import ensure_database


def copydb(ctx, source, dest):
    # drop database if exist
    ensure_database(ctx, dest, state="absent")

    # Copy database
    ensure_database(ctx, dest, state="present", template=source)

    main_path = ctx.obj["filestore_folder_path"] / "filestore"
    source_path = main_path / source
    dest_path = main_path / dest
    # Drop filestore if exist
    logger.info(f"Remove filestore of '{dest}' if exists.")
    shutil.rmtree(dest_path, ignore_errors=True)

    # Copy Filestore
    logger.info(f"Copy filestore of '{source}' into '{dest}' folder ...")
    shutil.copytree(source_path, dest_path)


def dropdb(ctx, database):
    """Drop a database and its filestore"""
    # Drop database
    logger.info(f"Drop database '{database}' if it exists...")
    ensure_database(ctx, database, state="absent")
    # Drop filestore
    root_filestore_path = ctx.obj["filestore_folder_path"] / "filestore"
    filestore_path = root_filestore_path / database
    logger.info(f"Remove filestore of '{database}' if exists...")
    shutil.rmtree(filestore_path, ignore_errors=True)

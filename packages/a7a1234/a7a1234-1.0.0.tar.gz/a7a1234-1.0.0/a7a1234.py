import argparse
from typing import Any

import uvicorn
import yaml
from loguru import logger
from src import app


def setup_arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Backend",
        description="For handling data",
    )
    parser.add_argument(
        "-c", "--config", help="location of the backend config file in yaml format."
    )
    args = parser.parse_args()
    logger.info(f"Python args: {args}")
    return args

def get_config_from_args(args: argparse.Namespace) -> Any:

    with open(args.config, "r") as config_file:
        config = yaml.safe_load(config_file)
        return config

def run_unicorn_app(config: Any) -> None:
    logger.info("Starting uvicorn server ...")
    port = int(config.get("BACKEND_PORT"))
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=port,
        log_config=config.get("UNVICORN_LOG_INI"),
    )
    logger.info(f"Started unvicorn server with {port=} ...")

if __name__ == "__main__":
    args: argparse.Namespace = setup_arg_parser()
    config: Any = get_config_from_args(args=args)
    run_unicorn_app(config=config)
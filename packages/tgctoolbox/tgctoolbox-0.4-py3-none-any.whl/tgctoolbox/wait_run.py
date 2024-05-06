import argparse
import asyncio
import os

import requests

from .logger import setup_custom_logger as TGCLoggerSetup

# Argument Parsing
parser = argparse.ArgumentParser(
    description="Check if a server is up with a maximum number of retries."
)
parser.add_argument(
    "--retries",
    type=int,
    default=5,
    help="Maximum number of retries to check if the server is up.",
)
parser.add_argument(
    "--host", type=str, default="localhost", help="Host of the server to check."
)
parser.add_argument(
    "--port", type=int, default=8000, help="Port of the server to check."
)

logger = TGCLoggerSetup("wait_run")


def is_server_up(host, port):
    """
    Check if the server is up and running and not throwing errors.

    This function attempts to make a GET request to the specified host and port.
    It returns the server status as 'up', 'down', or an error message depending on
    the server's response or a failure to connect.

    Args:
        host (str): The host name of the server.
        port (int): The port number of the server.

    Returns:
        str: 'up' if the server is running correctly, 'down' if the server is unreachable,
             or an error message if there's an issue with the server's response.
    """
    try:
        response = requests.get(f"http://{host}:{port}")
        if response.status_code == 200:
            return "up"
        else:
            return f"error with status code {response.status_code}"
    except requests.ConnectionError:
        return "down"
    except Exception as e:
        return f"error: {str(e)}"


async def wait_for_server(host, port, max_retries):
    """
    Asynchronously wait for a server to become available with a maximum retry limit.

    This function repeatedly checks if the server is up every 5 seconds up to a maximum
    number of retries. It prints the status of each attempt.

    Args:
        host (str): The host name of the server.
        port (int): The port number of the server.
        max_retries (int): The maximum number of retries for checking server status.

    """
    retries = 0
    while retries < max_retries:
        status = is_server_up(host, port)
        if status == "up":
            logger.info(f"Server at {host}:{port} is up and running!")
            return
        elif status == "down":
            logger.warning(
                f"Server at {host}:{port} is down. Retrying {retries+1}/{max_retries}..."
            )
        else:  # Error case
            logger.error(
                f"Server at {host}:{port} encountered an issue: {status}. Retrying {retries+1}/{max_retries}..."
            )

        retries += 1
        await asyncio.sleep(5)  # wait for 5 seconds before trying again

    logger.warning("Maximum retries reached. Server is not up.")


# Main Script
if __name__ == "__main__":
    """
    Main script for checking if a server is up.

    This script uses command-line arguments to set the host, port, and maximum number
    of retries for checking if a server is up. It leverages the `wait_for_server` function
    to perform the checks asynchronously.
    """
    args = parser.parse_args()

    HOST = args.host if args.host is not None else os.environ.get("HOST", "localhost")
    PORT = args.port if args.port is not None else os.environ.get("PORT", 8000)
    MAX_RETRIES = args.retries

    asyncio.run(wait_for_server(HOST, PORT, MAX_RETRIES))

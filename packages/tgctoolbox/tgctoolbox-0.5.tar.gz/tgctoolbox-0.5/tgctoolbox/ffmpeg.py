import subprocess
import sys

from .logger import setup_custom_logger as TGCLoggerSetup

logger = TGCLoggerSetup(__name__)


def is_admin():
    """_summary_: Checks if the current user is an administrator on Windows.

    Returns:
        bool: True if the current user is an administrator, False otherwise.
    """
    try:
        return (
            subprocess.check_call(
                ["net", "session"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            == 0
        )
    except:
        return False


def run_as_admin():
    """_summary_: Restarts the current script with administrator privileges on Windows.

    Raises:
        PermissionError: If the current user is not an administrator.
    """
    logger.info("Requesting administrator privileges...")
    subprocess.call(
        ["powershell", "Start-Process", "python", f"'{sys.argv[0]}'", "-Verb", "RunAs"]
    )
    sys.exit()


def is_choco_installed():
    """_summary_: Checks if Chocolatey is installed on Windows. Output of the command called to do so is supressed.

    Returns:
        bool: True if Chocolatey is installed, False otherwise.
    """
    try:
        return (
            subprocess.run(
                "choco -v",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            ).returncode
            == 0
        )
    except FileNotFoundError:
        return False


def is_ffmpeg_installed():
    """_summary_: Checks if FFmpeg is installed on Windows. Output of the command called to do so is supressed.

    Returns:
        bool: True if FFmpeg is installed, False otherwise.
    """
    try:
        return (
            subprocess.run(
                ["ffmpeg", "-version"], stdout=subprocess.DEVNULL, check=False
            ).returncode
            == 0
        )
    except FileNotFoundError:
        return False


def install_ffmpeg_windows(supress_output=False):
    """_summary_: Installs Chocolatey and FFmpeg on Windows. If the current user is not an administrator, the script will be restarted with administrator privileges.

    NOTE: This function is only intended to be called on Windows. Also, supress output only supresses stdout not stderr, for ease of debugging.

    Args:
        supress_output (bool, optional): Whether to supress the output of the commands called during installation. Defaults to False.
    """
    stdout = subprocess.DEVNULL if supress_output else None

    if not is_choco_installed() or not is_ffmpeg_installed():
        if not is_admin():
            run_as_admin()

        if not is_choco_installed():
            logger.info("Installing Chocolatey...")
            ps_command = "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
            subprocess.run(
                ["powershell", "-Command", ps_command], check=True, stdout=stdout
            )

        if not is_ffmpeg_installed():
            logger.info("Installing FFmpeg...")
            subprocess.run(["choco", "install", "ffmpeg"], check=True, stdout=stdout)

    else:
        logger.info("Chocolatey and FFmpeg are already installed.")


def install_ffmpeg_linux(supress_output=False):
    """_summary_: Installs Chocolatey and FFmpeg on Linux. Only tested on Unix containers, not live distro.

    NOTE: This function is only intended to be called on Linux. Also, supress output supresses both stdout and stderr.

    Args:
        supress_output (bool, optional): Whether to supress the output of the commands called during installation. Defaults to False.
    """
    try:
        stdout = subprocess.DEVNULL if supress_output else None

        # Check if FFmpeg is installed
        try:
            ffmpeg_check = subprocess.run(
                ["ffmpeg", "-version"], stdout=stdout, stderr=stdout, check=False
            )
            if ffmpeg_check.returncode != 0:
                raise FileNotFoundError("FFmpeg not found")
        except FileNotFoundError:
            logger.info("FFmpeg is not installed, installing now...")
            subprocess.run(
                ["sudo", "apt", "update"], check=True, stdout=stdout, stderr=stdout
            )
            subprocess.run(
                ["sudo", "apt", "install", "-y", "ffmpeg"],
                check=True,
                stdout=stdout,
                stderr=stdout,
            )
        else:
            logger.info("FFmpeg is already installed.")
    except subprocess.CalledProcessError as e:
        logger.error(
            f"Failed to install FFmpeg on Linux. Error: {str(e)}", exc_info=True
        )
        sys.exit(1)


def install_ffmpeg_macos(supress_output=False):
    """_summary_: Installs Chocolatey and FFmpeg on MacOS. This have not been tested.

    WARNING: This function have not been tested. It should theoretically work, but be warned that it might not.s

    Args:
        supress_output (bool, optional): _description_. Defaults to False.
    """
    try:
        stdout = subprocess.DEVNULL if supress_output else None

        # Check if Homebrew is installed
        if (
            subprocess.run("brew -v", shell=True, stdout=stdout, check=False).returncode
            != 0
        ):
            logger.info("Installing Homebrew...")
            subprocess.run(
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                check=True,
                shell=True,
            )

        # Check if FFmpeg is installed
        if (
            subprocess.run(
                "ffmpeg -version", shell=True, stdout=stdout, check=False
            ).returncode
            != 0
        ):
            logger.info("Installing FFmpeg...")
            subprocess.run(["brew", "install", "ffmpeg"], check=True)
        else:
            logger.info("FFmpeg is already installed.")
    except subprocess.CalledProcessError:
        logger.error("Failed to install FFmpeg on macOS.", exc_info=True)
        sys.exit(1)

import datetime
import subprocess
from .print import cprint


def get_current_datetime(format="%Y-%m-%d %H:%M:%S"):
    # Return current date and time
    # Default format: yyyy-mm-dd HH:MM:SS
    # "%Y-%m-%d %H:%M:%S" -> yyyy-mm-dd HH:MM:SS
    # "%m-%d-%Y" -> mm-dd-yyyy
    now = datetime.datetime.now()
    now = now.strftime(format)
    return now


def format_date(input_date, input_format, output_format):
    # Parse the input string as a date
    date_object = datetime.datetime.strptime(input_date, input_format)

    # Format the date in the desired format
    return date_object.strftime(output_format)


def has_numbers(input):
    return any(char.isdigit() for char in input)


def terminate_app(app_name):
    try:
        # Use the 'taskkill' command on Windows to terminate the application
        subprocess.run(["taskkill", "/F", "/IM", app_name], check=True)

        # If you're on a Unix-based system (Linux or macOS), you can use 'pkill'
        # subprocess.run(['pkill', app_name], check=True)

        cprint(f"<g>Successfully terminated {app_name}")
    except subprocess.CalledProcessError as e:
        cprint(f"<r>Failed to terminate {app_name}: {e}")

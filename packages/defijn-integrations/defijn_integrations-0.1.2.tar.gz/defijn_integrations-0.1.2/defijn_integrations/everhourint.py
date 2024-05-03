from pathlib import Path

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from json.decoder import JSONDecodeError
from rich.console import Console
import datetime

console = Console()

API_EVERHOUR_KEY_FILE = Path.home() / ".everhour_api_key"


def load_everhour_api_key():
    if API_EVERHOUR_KEY_FILE.exists():
        return API_EVERHOUR_KEY_FILE.read_text().strip()
    else:
        return None


def save_everhour_api_key(api_key):
    API_EVERHOUR_KEY_FILE.write_text(api_key)


def get_everhour_user_id(api_key):
    try:
        with console.status("[bold magenta]Getting user ID..", spinner="monkey"):
            headers = {"X-Api-Key": api_key}
            response = requests.get("https://api.everhour.com/users/me", headers=headers)
            response.raise_for_status()
            return response.json()["id"]

    except HTTPError as http_err:
        console.print(f"[bold red]HTTP error occurred: {http_err}[/]")  # HTTP error
    except ConnectionError as conn_err:
        console.print(f"[bold red]Connection error occurred: {conn_err}[/]")  # Network problem
    except Timeout as timeout_err:
        console.print(f"[bold red]Timeout error occurred: {timeout_err}[/]")  # Request timeout
    except JSONDecodeError as json_err:
        console.print(f"[bold red]JSON decode error: {json_err}[/]")  # JSON decoding problem
    except RequestException as req_err:
        console.print(f"[bold red]An error occurred during the request: {req_err}[/]")  # Other request issues
    except Exception as err:
        console.print(f"[bold red]An unexpected error occurred: {err}[/]")  # Other exceptions

    return None  # Return None if any exception occurred


def get_everhour_project(project_id, api_key):
    # console.print("[bold magenta]Getting project name...[/]")
    headers = {"X-Api-Key": api_key}
    response = requests.get(f"https://api.everhour.com/projects/{project_id}", headers=headers)
    response.raise_for_status()
    return response.json()["name"]


def get_everhour_previous_day_time(user_id, api_key):
    # console.print("[bold magenta]Getting previous day's time...[/]")
    with console.status("[bold magenta]Getting previous day's time..", spinner="dots"):
        headers = {"X-Api-Key": api_key}
        previous_day_work = []

        # if today is Monday, get time from Friday to Sunday
        if datetime.datetime.today().weekday() == 0:
            # MONDAY
            print("Today is Monday - getting time from Friday to Sunday")

            yesterday = datetime.datetime.now() - datetime.timedelta(days=3)
            yesterday = yesterday.strftime("%Y-%m-%d")

            now = datetime.datetime.now() - datetime.timedelta(days=1)
            now = now.strftime("%Y-%m-%d")
        else:
            # NOT MONDAY
            yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
            yesterday = yesterday.strftime("%Y-%m-%d")
            now = datetime.datetime.now().strftime("%Y-%m-%d")

        # now = datetime.datetime.now().strftime("%Y-%m-%d")

        url = f"https://api.everhour.com/users/{user_id}/time?from={yesterday}&to={now}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            time_entries = response.json()
            for time_entry in time_entries:
                project_name = get_everhour_project(time_entry["task"]["projects"][0], api_key)
                project_obj = {"project_name": project_name, "work": []}
                if project_obj not in previous_day_work:
                    previous_day_work.append(project_obj)
            for time_entry in time_entries:
                project_name = get_everhour_project(time_entry["task"]["projects"][0], api_key)
                obj = {"task_name": time_entry["task"]["name"]}
                for project in previous_day_work:
                    if project["project_name"] == project_name:
                        if obj not in project["work"]:
                            project["work"].append(obj)
            return previous_day_work
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")


def update_everhour_api_key():
    console.print("[bold yellow]Updating API Key...[/]")
    new_key = console.input("[bold magenta]Enter your new Everhour API Key: [/]")
    save_everhour_api_key(new_key)
    console.print("[bold green]API Key updated successfully![/]")

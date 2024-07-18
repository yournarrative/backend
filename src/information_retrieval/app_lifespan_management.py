import marvin
from starlette.datastructures import State

from information_retrieval.connectors.cohere.client import create_cohere_client
from information_retrieval.connectors.supabase.client import create_supabase_client
from information_retrieval.utils.files import load_config_from_env, load_env


async def init_app_state(state: State):
    # Load env variables
    state.env = load_env()

    # Load config
    state.config = load_config_from_env(
        env=state.env.get("ENVIRONMENT"),
    )
    request()
    debug_test()

    state.cohere_client = create_cohere_client(
        state=state,
    )

    state.supabase_client = create_supabase_client(
        url=state.env.get("SUPABASE_URL"), key=state.env.get("SUPABASE_KEY"),
    )

    init_marvin_api_key(state)


def init_marvin_api_key(state: State):
    marvin.settings.openai.api_key = state.env.get("OPENAI_API_KEY")


async def cleanup_app_state(state: State):
    pass


def request():
    import requests

    def fetch_wikipedia_main_page():
        url = "https://en.wikipedia.org/wiki/Main_Page"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            print("Successfully fetched the Wikipedia main page.")
            print("Status Code:", response.status_code)
            print("Content Type:", response.headers['Content-Type'])
            # Print a portion of the content for demonstration purposes
            print("Content:", response.text[:500])  # Print the first 500 characters
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the Wikipedia main page: {e}")

    fetch_wikipedia_main_page()


def debug_test():
    import socket

    def resolve_dns(url):
        try:
            result = socket.gethostbyname(url)
            print(f"DNS resolution for {url}: {result}")
        except socket.gaierror as e:
            print(f"Error resolving DNS for {url}: {e}")

    resolve_dns("google.com")
    resolve_dns("https://google.com")
    resolve_dns("wikipedia.com")
    resolve_dns("https://wikipedia.com")
    resolve_dns("nkdjutovalclevvlnagr.supabase.co")
    resolve_dns("https://nkdjutovalclevvlnagr.supabase.co")
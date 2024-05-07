import asyncio
import os

import click
from dotenv import load_dotenv
from httpx import AsyncClient

from exponent.core.config import get_settings
from exponent.core.remote_execution.client import RemoteExecutionClient

load_dotenv()


@click.group()
def cli() -> None:
    """Exponent CLI group."""
    pass


@cli.command()
@click.option("--key", help="Your Exponent API Key")
def login(key: str) -> None:
    settings = get_settings()
    if not key:
        click.echo("No API Key detected, redirecting to login...")
        click.launch(f"{settings.base_url}/")
        return
    click.echo("Saving API Key to ~/.exponent...")
    if settings.api_key and settings.api_key != key:
        click.confirm("Detected existing API Key, continue? ", default=True, abort=True)
    with open(os.path.expanduser("~/.exponent"), "a") as f:
        f.write(f"\nEXPONENT_API_KEY={key}\n")
    click.echo("API Key saved.")


@cli.command()
@click.option(
    "--chat-id", help="ID of an existing chat session to reconnect", required=False
)
def run(chat_id: str | None = None) -> None:
    settings = get_settings()
    if not settings.api_key:
        click.echo("No API Key detected, redirecting to login...")
        click.launch(f"{settings.base_url}/")
        return
    else:
        api_key = settings.api_key

    loop = asyncio.get_event_loop()
    task = loop.create_task(
        start_client(api_key, settings.base_url, settings.base_api_url, chat_id)
    )
    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        task.cancel()
        try:
            loop.run_until_complete(task)
        except asyncio.CancelledError:
            pass


async def start_client(
    api_key: str, base_url: str, base_api_url: str, chat_id: str | None = None
) -> None:
    if not chat_id:
        async with AsyncClient() as api_client:
            client = RemoteExecutionClient(api_key, base_api_url, api_client)
            chat_id = (await client.create_chat()).chat_uuid

    click.echo()
    click.secho("△ Exponent v1.0.0", fg=(180, 150, 255), bold=True)
    click.echo()
    click.echo(
        "  - Link: " + click.style(f"{base_url}/chats/{chat_id}", fg=(100, 200, 255))
    )
    click.echo(click.style("  - Shell: /bin/zsh", fg="white"))
    click.echo()
    click.echo(click.style("✓", fg="green", bold=True) + " Ready in 1401ms")

    try:
        async with AsyncClient() as api_client:
            execution_client = RemoteExecutionClient(api_key, base_api_url, api_client)
            await run_execution_client(execution_client, chat_id)
    except Exception:
        click.echo("Unexpected error.")


async def run_execution_client(client: RemoteExecutionClient, chat_uuid: str) -> None:
    while True:
        execution_requests = await client.get_execution_requests(chat_uuid)
        for execution_request in execution_requests:
            execution_response = client.execute_code(execution_request)
            await client.post_execution_result(chat_uuid, execution_response)
        await asyncio.sleep(0.05)


if __name__ == "__main__":
    cli()

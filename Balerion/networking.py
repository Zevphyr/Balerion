import logging
import aiohttp


networking_client = aiohttp.ClientSession


async def get(url):
    """ Builds a request as the bot to request anything through HTTP
    :param url:
        The url to fetch
    :return:
        Response content in bytes or '' if an error occurs
    """

    global networking_client  # Use the Bot network instance

    try:
        async with networking_client.get(url) as resp:
            content = await resp.text()
            return content
    except aiohttp.ClientConnectionError:
        logging.error('Failed to fetch page %s', url)
        return ''

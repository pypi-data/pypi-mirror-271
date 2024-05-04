"""
Integrations with OpenAI API.

This handles the connection and a backup account in case we run out of requests.
"""
import logging
import pathlib
import re

from litellm import completion

from . import settings

logger = logging.getLogger()


def resolve_kwargs() -> dict:
    """
    Resolve the non-None values from the settings to pass to the completion function
    :return: dict
    """
    return {
        k: v
        for k, v in settings.LITELLM.items()
        if v is not None
    }


def get_completion(messages, **kwargs):
    """
    Get a completion from the openai API
    :param messages: The messages to send to the API
    :param kwargs: Additional arguments to pass to the completion function
    :return: The completion
    """
    _kwargs = resolve_kwargs()
    _kwargs.update(kwargs)
    response = completion(
        messages=messages,
        **_kwargs
    )
    return response.choices[0].message.content


def get_file_completion(file_path: pathlib.Path, **kwargs):
    """
    For a file on disk, resolve the prompt, open the file, and get a completion.
    :param file_path: The path to the file containing the code to document
    :return: The completion
    """
    # Check that the file_path extension is in the list of supported extensions
    _ext = file_path.suffix
    if _ext not in settings.EXTENSIONS:
        logger.debug(f'Skipping unsupported file type: {file_path}')
        return None
    code = file_path.read_text()
    prompt = settings.PROMPT
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": code},
    ]
    return get_completion(messages, **kwargs)


CODE_BLOCK_START_REGEX = re.compile(r'```[a-z]*\n')


def parsed_file_completion(file_path: pathlib.Path, **kwargs):
    """
    Runs the file completion but then parses out the actual response
    that is usable for documentation.
    :param file_path: The path to the file containing the code to document
    :return: The completion
    """
    completion = get_file_completion(file_path, **kwargs)
    cleaned = completion.split(settings.ESCAPE_CHARACTERS)[1]
    if CODE_BLOCK_START_REGEX.match(cleaned):
        # Replace the first code block with the completion
        cleaned = CODE_BLOCK_START_REGEX.sub('', cleaned, count=1).rstrip('```')

    return cleaned

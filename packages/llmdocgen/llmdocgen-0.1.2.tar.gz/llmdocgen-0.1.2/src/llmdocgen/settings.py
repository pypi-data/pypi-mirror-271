"""
Settings for the project

You may set up connections to OpenAI, Anthropic, and other LLM service providers here
"""
import os
import pathlib

import attrdict
import environs

ENV_PATH = os.environ.get('LLMDOCGEN_ENV_PATH', '~/.llmdocgen')
ENV_PATH = pathlib.Path(ENV_PATH).expanduser()

env = environs.Env()
env.read_env(str(ENV_PATH))

_file = pathlib.Path(__file__).resolve()

# Setup authentication by setting environment variables for LiteLLM
# See this for more details: https://docs.litellm.ai/docs/

# We simply pull the model, api_base, and other arguments we need to run completions
# from the environment variables
# If not set, we do not pass it in and the default values from litellm will be used
LITELLM = attrdict.AttrDict(
    model=env.str('LITELLM_MODEL', 'claude-3-opus-20240229'),
    api_base=env.str('LITELLM_API_BASE', None),
    timeout=env.float('LITELLM_TIMEOUT', None),
    temperature=env.float('LITELLM_TEMPERATURE', None),
    top_p=env.float('LITELLM_TOP_P', None),
    n=env.int('LITELLM_N', None),
    max_tokens=env.int('LITELLM_MAX_TOKENS', None),
    presence_penalty=env.float('LITELLM_PRESENCE_PENALTY', None),
    frequency_penalty=env.float('LITELLM_FREQUENCY_PENALTY', None),
    logit_bias=env.float('LITELLM_LOGIT_BIAS', None),
    user=env.str('LITELLM_USER', None),
    seed=env.int('LITELLM_SEED', None),
    tools=env.list('LITELLM_TOOLS', None),
    tool_choice=env.str('LITELLM_TOOL_CHOICE', None),
    logprobs=env.bool('LITELLM_LOGPROBS', None),
    top_logprobs=env.int('LITELLM_TOP_LOGPROBS', None),
    deployment_id=env.str('LITELLM_DEPLOYMENT_ID', None),
)

PROMPT_FILE_PATH = env.path('PROMPT_FILE', _file.parent / 'default_prompt.txt')
PROMPT_FILE = pathlib.Path(PROMPT_FILE_PATH)
assert PROMPT_FILE.exists(), f'Prompt file does not exist: {PROMPT_FILE}'
PROMPT = PROMPT_FILE.read_text()

# These should be specified in your prompt and will be used to parse the output.
# They are used to determine the start and end of the completion.
# Do not use character sequences that appear in your code as we look for these
# At the beginning and end of the completion.
# If not set, we will simply use the entire completion as the output.
ESCAPE_CHARACTERS = env.str('ESCAPE_CHARACTERS', '%"%"%')

# The following are file types that we will document
# Some formats (eg json) do not support comments, so we will not document them
DEFAULT_EXTENSIONS = [
    '.py',     # Python
    '.js',     # JavaScript
    '.ts',     # TypeScript
    '.html',   # HTML
    '.css',    # CSS
    '.yaml',   # YAML
    '.yml',    # YAML
    '.xml',    # XML
    '.c',      # C
    '.cpp',    # C++
    '.cs',     # C#
    '.h',      # C/C++ header
    '.hpp',    # C++ header
    '.java',   # Java
    '.php',    # PHP
    '.rb',     # Ruby
    '.go',     # Go
    '.rs',     # Rust
    '.swift',  # Swift
    '.kt',     # Kotlin
    '.scala',  # Scala
    '.sh',     # Shell script
    '.bash',   # Bash script
    '.pl',     # Perl
    '.pm',     # Perl module
    '.t',      # Perl test file
    '.pod',    # Perl documentation
    '.sql',    # SQL
    '.lua',    # Lua
    '.m',      # MATLAB
    '.r',      # R
    '.rmd',    # R Markdown
    '.f90',    # Fortran
    '.f95',    # Fortran
    '.f03',    # Fortran
    '.f08',    # Fortran
    '.hs',     # Haskell
    '.lhs',    # Literate Haskell
    '.pas',    # Pascal
    '.pl',     # Prolog
    '.pro',    # Prolog
    '.v',      # Verilog
    '.vhd',    # VHDL
    '.sv',     # SystemVerilog
    '.adb',    # Ada
    '.ads',    # Ada
    '.asm',    # Assembly
    '.s',      # Assembly
    '.cl',     # Common Lisp
    '.lisp',   # Common Lisp
    '.el',     # Emacs Lisp
    '.vim',    # Vim script
    '.tcl',    # Tcl
    '.erl',    # Erlang
    '.hrl',    # Erlang header
    '.fs',     # F#
    '.fsx',    # F# script
    '.ino',    # Arduino
    '.pde',    # Processing
]

# You can add additional file extensions to document here
EXTRA_EXTENSIONS = env.list('LLMDOCGEN_EXTRA_EXTENSIONS', [])

# You can override the default extensions by setting the SUPERDOC_EXTENSIONS environment variable
# If you do not set this, we will use the default extensions + any extra extensions you have added
EXTENSIONS = env.list('LLMDOCGEN_EXTENSIONS', DEFAULT_EXTENSIONS + EXTRA_EXTENSIONS)

SAVE_BY_DEFAULT = env.bool('LLMDOCGEN_SAVE_BY_DEFAULT', False)

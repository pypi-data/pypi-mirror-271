# Checol

This tool is designed to analyze Git repository diffs and Prisma schema files, and generate related text responses using the AI model. It enables you to get detailed explanations, clarifications, or SQL code based on Git changes or Prisma schema files from the AI.

## Prerequisites

- Python 3.8 or higher
- Access to a Git local repository
- Prisma schema file

## Installation

```
pip install checol
```

## Configuration

1. Set your Anthropic API key in the environment variable `ANTHROPIC_API_KEY`.

    ```
    export ANTHROPIC_API_KEY='your_api_key_here'
    ```

2. (Optional) If you want to change the default AI model, also set `ANTHROPIC_API_MODEL`.

    ```
    export ANTHROPIC_API_MODEL='claude-3-haiku-20240307'
    ```

## Usage

### Analyzing Git diffs

1. Use the `diff` command to analyze Git diffs and start interacting with Claude.

    ```
    checol diff [git diff options]
    ```

2. Follow the prompts to input your description or questions regarding the Git diffs.

3. Review the response from Claude and continue the interaction as desired.

### Generating SQL from Prisma schema

1. Use the `prismaQuery` command to generate SQL from a Prisma schema file.

    ```
    checol prismaQuery path/to/your/schema.prisma
    ```

2. Follow the prompts to provide any additional context or instructions to the AI.

3. Review the generated SQL response from Claude and continue the interaction as needed.

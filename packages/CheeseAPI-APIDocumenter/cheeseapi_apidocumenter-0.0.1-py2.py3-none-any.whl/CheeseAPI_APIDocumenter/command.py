import os, json, re
from typing import Literal

import click
from CheeseAPI import app
from CheeseLog import logger

from CheeseAPI_APIDocumenter.documenter import routes

@click.command()
@click.option('--app', '_app', default = 'app', help = 'CheeseAPI entry file (Default "app")')
@click.option('--outputPath', 'outputPath', default = './document/', help = 'API document output path, based app.workspace.base (Default "./document/", support absolute path and relative path)')
@click.option('--outputType', 'outputType', type = click.Choice(['RAW', 'MD']), default = 'MD', help = 'Output file type. RAW: raw file, for any API interface file in Documenter format; MD: markdown; (Default "MD")')
def command(_app: str, outputPath: str, outputType: Literal['RAW', 'MD']):
    os.environ['CheeseAPI_Documenter'] = ''

    exec(f'import {_app}')
    app.workspace.logger = False
    app._handle.loadLocalModules()

    os.makedirs(os.path.join(app.workspace.base, outputPath) if outputPath[0] == '.' else outputPath, exist_ok = True)

    if outputType == 'RAW':
        with open(os.path.join(app.workspace.base, outputPath, 'raw.json') if outputPath[0] == '.' else os.path.join(outputPath, f'{key}'), 'w', encoding = 'utf-8') as f:
            json.dump(routes, f, indent = 4)

    print()
    i = 0
    for key, _routes in routes.items():
        message, styledMessage = app._text.progressBar(i / len(routes))
        logger.loading(f'API Documents: {message} {key}', f'API Documents: {styledMessage} {key}')
        i += 1

        if outputType == 'MD':
            with open(os.path.join(app.workspace.base, outputPath, f'{key}.md') if outputPath[0] == '.' else os.path.join(outputPath, f'{key}'), 'w', encoding = 'utf-8') as f:
                f.write(f'# **{key}**\n')

                for route in _routes:
                    f.write(f'\n## **`{' & '.join(route["methods"])} {route["path"]}`**\n')

                    if route['description']:
                        f.write(f'\n{route["description"]}\n')

                    if route['request']:
                        f.write('\n- **Request**\n')

                        if 'path' in route['request']:
                            f.write(f'\n    - **Path**\n')

                            for param in route['request']['path']['params']:
                                f.write(f'\n        - **`{param["key"]}: {param.get("type", "str")}`**\n')

                                if 'description' in param:
                                    f.write(f'\n            {re.sub(r"\n(?!\n)", '\n            ', param["description"])}\n')

                        if 'query' in route['request']:
                            f.write(f'\n    - **Query**\n')

                            for param in route['request']['query']['params']:
                                f.write(f'\n        - **`{param["key"]}: {param.get("type", "str")}')

                                if 'default' in param:
                                    f.write(f' = {param["default"]}')

                                f.write('`**')

                                if param.get('required', True):
                                    f.write(f' <sub style="color: red; font-weight: bold;">*</sub>')

                                f.write(f'\n')

                                if 'description' in param:
                                    f.write(f'\n            {re.sub(r"\n(?!\n)", '\n            ', param["description"])}\n')

                        if 'headers' in route['request']:
                            f.write(f'\n    - **Headers**\n')

                            for param in route['request']['headers']['params']:
                                f.write(f'\n        - **`{param["key"]}: {param.get("type", "str")}')

                                if 'default' in param:
                                    f.write(f' = {param["default"]}')

                                f.write('`**')

                                if param.get('required', True):
                                    f.write(f' <sub style="color: red; font-weight: bold;">*</sub>')

                                f.write(f'\n')

                                if 'description' in param:
                                    f.write(f'\n            {re.sub(r"\n(?!\n)", '\n            ', param["description"])}\n')

                        if 'body' in route['request']:
                            f.write(f'\n    - **Body**\n')

                            f.write(f'\n        type: {route["request"]["body"].get("type", "text")}\n')

                            if route['request']['body'].get('type', 'text') in ['bytes', 'text']:
                                f.write(f'\n        {re.sub(r"\n(?!\n)", '\n        ', param["description"])}\n')

                            elif route['request']['body'].get('type', 'text') in ['form-data', 'urlencoded']:
                                for param in route['request']['body']['params']:
                                    f.write(f'\n        - **`{param["key"]}: {param.get("type", "str")}')

                                    if 'default' in param:
                                        f.write(f' = {param["default"]}')

                                    f.write('`**')

                                    if param.get('required', True):
                                        f.write(f' <sub style="color: red; font-weight: bold;">*</sub>')

                                    f.write(f'\n')

                                    if 'description' in param:
                                        f.write(f'\n            {re.sub(r"\n(?!\n)", '\n            ', param["description"])}\n')

                        if 'cookie' in route['request']:
                            f.write(f'\n    - **Cookie**\n')

                            for param in route['request']['cookie']['params']:
                                f.write(f'\n        - **`{param["key"]}: {param.get("type", "str")}')

                                if 'default' in param:
                                    f.write(f' = {param["default"]}')

                                f.write('`**')

                                if param.get('required', True):
                                    f.write(f' <sub style="color: red; font-weight: bold;">*</sub>')

                                f.write(f'\n')

                                if 'description' in param:
                                    f.write(f'\n            {re.sub(r"\n(?!\n)", '\n            ', param["description"])}\n')

                        if 'subprotocols' in route['request']:
                            f.write(f'\n    - **Subprotocols**\n')
                            f.write(f'\n        {re.sub(r"\n(?!\n)", '\n        ', route["request"]["subprotocols"]["description"])}\n')

                    if 'response' in route:
                        f.write('\n- **Response**\n')
                        for response in route['response']:
                            f.write(f'\n    - **{response.get("status", 200)}**\n')

                            if 'description' in response:
                                f.write(f'\n        {re.sub(r"\n(?!\n)", '\n        ', response["description"])}\n')

                            if 'headers' in response:
                                f.write(f'\n    - **Headers**\n')

                                for param in response['headers']['params']:
                                    f.write(f'\n        - **`{param["key"]}: {param.get("type", "str")}`**')

                                    if param.get('nullable', True):
                                        f.write(f' <sub style="color: red; font-weight: bold;">*</sub>')

                                    f.write(f'\n')

                                    if 'description' in param:
                                        f.write(f'\n            {re.sub(r"\n(?!\n)", '\n            ', param["description"])}\n')

                            if 'body' in response:
                                f.write(f'\n        - **`Body: {response["body"].get("type", "text")}`**\n')

                                if 'description' in response['body']:
                                    f.write(f'\n            {re.sub(r"\n(?!\n)", '\n            ', response["body"]["description"])}\n')

                            if 'cookie' in response:
                                f.write(f'\n        - **Cookie**\n')

                                for param in response['cookie']['params']:
                                    f.write(f'\n            - **`{param["key"]}: {param.get("type", "str")}`**')

                                    if param.get('nullable', True):
                                        f.write(f' <sub style="color: red; font-weight: bold;">*</sub>')

                                    f.write(f'\n')

                                    if 'description' in param:
                                        f.write(f'\n                {re.sub(r"\n(?!\n)", '\n                ', param["description"])}\n')

                            if 'example' in response:
                                f.write('\n        - **Example**\n')
                                f.write(f'\n            {re.sub(r"\n(?!\n)", '\n            ', route["Example"])}\n')

                    if 'example' in route:
                        f.write('\n- **Example**\n')
                        f.write(f'\n    {re.sub(r"\n(?!\n)", '\n    ', route["Example"])}\n')

    logger.loaded(f'''API Documents:
{' | '.join(routes.keys())}''', refreshed = True)

if __name__ == '__main__':
    command()

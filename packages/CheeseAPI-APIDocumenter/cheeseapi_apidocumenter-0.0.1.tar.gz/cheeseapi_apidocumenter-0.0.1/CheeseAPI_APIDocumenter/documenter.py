import os, http
from typing import List, TypedDict, Dict, Literal, Any, NotRequired, overload

class Route(TypedDict):
    path: str
    methods: List[http.HTTPMethod | str]
    description: str

    class Request(TypedDict):
        class Path(TypedDict):
            class Param(TypedDict):
                key: str
                type: NotRequired[Literal['str', 'int', 'float', 'uuid']]
                description: NotRequired[str]
            params: List[Param]
        path: NotRequired[Path]

        class Query(TypedDict):
            class Param(TypedDict):
                key: str
                type: NotRequired[Literal['str', 'bool', 'int', 'float', 'timestamp', 'mail', 'uuid', 'list', 'dict']]
                required: NotRequired[bool]
                default: NotRequired[Any]
                description: NotRequired[str]
            params: List[Param]
        query: NotRequired[Query]

        class Header(TypedDict):
            class Param(TypedDict):
                key: str
                type: NotRequired[Literal['str', 'bool', 'int', 'float', 'uuid']]
                required: NotRequired[bool]
                default: NotRequired[Any]
                description: NotRequired[str]
            params: List[Param]
        headers: NotRequired[Header]

        class Body(TypedDict):
            type: NotRequired[Literal['bytes', 'text', 'form-data', 'urlencoded']]
            description: NotRequired[str]
            class Param(TypedDict):
                key: str
                type: NotRequired[Literal['str', 'bool', 'int', 'float', 'timestamp', 'mail', 'uuid', 'file', 'list', 'dict']]
                required: NotRequired[bool]
                default: NotRequired[Any]
                description: NotRequired[str]
            params: List[Param]
        body: NotRequired[Body]

        class Cookie(TypedDict):
            class Param(TypedDict):
                key: str
                type: NotRequired[Literal['str', 'bool', 'int', 'float', 'timestamp', 'mail', 'uuid', 'list', 'dict']]
                required: NotRequired[bool]
                default: NotRequired[Any]
                description: NotRequired[str]
            params: List[Param]
        cookie: NotRequired[Cookie]
    request: Request | None

    class Response(TypedDict):
        status: NotRequired[http.HTTPStatus | int]
        description: NotRequired[str]

        class Header(TypedDict):
            class Param(TypedDict):
                key: str
                type: NotRequired[Literal['str', 'bool', 'int', 'float', 'uuid']]
                nullable: NotRequired[bool]
                description: NotRequired[str]
            params: List[Param]
        headers: NotRequired[Header]

        class Body(TypedDict):
            type: NotRequired[Literal['text', 'bytes', 'json', 'file']]
            description: str
        body: NotRequired[Body]

        class Cookie(TypedDict):
            class Param(TypedDict):
                key: str
                type: NotRequired[Literal['str', 'bool', 'int', 'float', 'timestamp', 'mail', 'uuid', 'list', 'dict']]
                nullable: NotRequired[bool]
                description: NotRequired[str]
            params: List[Param]
        cookie: NotRequired[Cookie]

        example: NotRequired[str]
    response: List[Response]

class Websocket(TypedDict):
    path: str
    methods: List[http.HTTPMethod | str]
    description: str

    class Request(TypedDict):
        class Path(TypedDict):
            class Param(TypedDict):
                key: str
                type: NotRequired[Literal['str', 'int', 'float', 'uuid']]
                description: NotRequired[str]
            params: List[Param]
        path: NotRequired[Path]

        class Query(TypedDict):
            class Param(TypedDict):
                key: str
                type: NotRequired[Literal['str', 'bool', 'int', 'float', 'timestamp', 'mail', 'uuid', 'list', 'dict']]
                required: NotRequired[bool]
                default: NotRequired[Any]
                description: NotRequired[str]
            params: List[Param]
        query: NotRequired[Query]

        class Subprotocols(TypedDict):
            description: str
        subprotocols: NotRequired[Subprotocols]

    example: NotRequired[str]

routes: Dict[str, List[Route | Websocket]] = {}

@overload
def documenter(description: str = '', request: Route.Request | None = None, response: List[Route.Response] = []):
    '''
    注册一个HTTP接口文档。

    ```python
    from CheeseAPI import app
    from CheeseAPI_APIDocumenter import documenter

    @documenter('注册用户', {
        'body': {
            'type': 'form-data',
            'params': [
                {
                    'key': 'username',
                    'type': 'str',
                    'description': '用户名；长度为5-20。'
                },
                {
                    'key': 'password',
                    'type': 'str',
                    'description': '由sha256一次加密后的密码。'
                },
                {
                    'key': 'gender',
                    'type': 'str',
                    'default': '"UNKNOWN"',
                    'description': '支持“MALE”、“FEMALE”和“UNKNOWN”。'
                },
                {
                    'key': 'birthDate',
                    'type': 'timestamp',
                    'required': True,
                    'description': '出生日期。'
                }
            ]
        }
    }, [
        {
            'status': 201,
            'description': '注册成功',
            'body': {
                'type': 'text',
                'description': '该用户的uuid。'
            }
        },
        {
            'status': 409,
            'description': '该用户名已被注册'
        }
    ])
    @app.route.post('/register')
    async def register(**_):
        ...
    ```
    '''

@overload
def documenter(description: str = '', request: Websocket.Request | None = None, example: str | None = None):
    ...

def documenter(description: str = '', request: Route.Request | None = None, arg1 = None, *, response: List[Route.Response] = [], example: str | None = None):
    def wrapper(fn):
        if os.getenv('CheeseAPI_Documenter') is not None:
            module = fn.__module__.split('.')[0] if '.' in fn.__module__ else 'index'
            if module not in routes:
                routes[module] = []

            if 'WEBSOCKET' in fn.routeMethods:
                routes[module].append({
                    'path': fn.routePath,
                    'methods': fn.routeMethods,
                    'description': description,
                    'request': request,
                    'example': arg1 or example
                })
            else:
                routes[module].append({
                    'path': fn.routePath,
                    'methods': [ http.HTTPMethod(method) if isinstance(method, str) else method for method in fn.routeMethods ],
                    'description': description,
                    'request': request,
                    'response': arg1 or response
                })

        return fn
    return wrapper

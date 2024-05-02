The World Anvil API Python Client is a wrapper client designed to work with the Boromir API released by World Anvil on August 26, 2023. Please note that this client is currently a work in progress and may not have all features implemented. The World Anvil API enables users to interact with the World Anvil database by utilizing various API endpoints.

> NOTE: If you find any issues feel free to open an issue and I will try to fix it. 

The latest version compatible with Aragorn is `0.12.1`. However, please be aware that the developer will not maintain the Aragorn version of the client. For Boromir, the latest version is recommended.

<details>
<summary>Latest</summary>

For the latest Boromir API Documentation, please visit:

- [Boromir API Documentation](https://www.worldanvil.com/api/external/boromir/documentation) 
- [Boromir API Swagger Documentation](https://www.worldanvil.com/api/external/boromir/swagger-documentation)
</details>

<details>
<summary>Older Versions</summary>

The Aragorn API is deprecated and will be removed in the future. However, if needed, you can still access the Aragorn API Documentation here:
    
- [Aragorn API Documentation](https://www.worldanvil.com/api/aragorn/documentation)
</details>

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Exceptions](#exceptions)
- [Classes](#classes)

## Installation

The package is published on PyPI and can be installed with pip. To install, run:

```python
pip --install pywaclient
```

## Usage

Below is a simple example on how to use the endpoints:

```python
import os
from pywaclient.api import BoromirApiClient

client = BoromirApiClient(
    '<YourScriptName>',
    '<link-to-your-website-or-bot-repository>',
    '<version>',
    os.environ['WA_APPLICATION_KEY'],
    os.environ['WA_AUTH_TOKEN']
)

# get your own user id. It is not possible to discover the user ids of other users via the API.
authenticated_user = client.user.identity()

# get the references to all the worlds on your account.
worlds = [world for world in client.user.worlds(authenticated_user['id'])]

# get the references to all the category on the first world.
categories = [category for category in client.world.categories(worlds[0]['id'])]

# gets a list of all the articles without a category in the first world
articles = [article for article in client.category.articles(worlds[0]['id'], '-1')]

# gets the full content of the first article
article = client.article.get(articles[0]['id'], 2)

# gets the full content of the first category. Categories and most other resources do not have a granularity of 2.
category = client.category.get(categories[0]['id'], 1)
```

## Endpoints

The `BoromirApiClient` class in the **api.py** file includes the following endpoints:

| **Endpoint**   | **con't.**           |
|----------------|----------------------|
| /article       | /map                 |
| /block         | /markertype          |
| /blockfolder   | /notebook            |
| /blocktemplate | /rpgsystem           |
| /canvas        | /secret              |
| /category      | /subscribergroup     |
| /chronicle     | /timeline            |
| /history       | /user                |
| /image         | /variable_collection |
| /manuscript    | /world               |

Additionally, the endpoints directory contains several Python files each representing a specific endpoint of the World Anvil API. This includes articles, blocks, categories, histories, images, maps, secrets, timelines, users, worlds, and more. Each file contains a class with methods for interacting with the respective endpoint.

## Exceptions

The **exceptions.py** file includes a series of exception classes to handle different types of errors:

| **Exception Class**           | **Description**                         |
|-------------------------------|-----------------------------------------|
| **WorldAnvilClientException** | Base exception class.                   |
| **WorldAnvilServerException** | Unsuccessful server response.           |
| **ConnectionException**       | Connection problem with the API server. |
| **UnexpectedStatusException** | Unexpected status code from server.     |
| **InternalServerException**   | Server responded with a 500 status.     |
| **UnauthorizedRequest**       | The request was not authorized.         |
| **AccessForbidden**           | Access to resource is forbidden.        |
| **ResourceNotFound**          | The requested resource was not found.   |
| **UnprocessableDataProvided** | Unprocessable data was provided.        |
| **FailedRequest**             | The request failed.                     |

Each of these exception classes are used to handle specific types of errors that may arise when using the World Anvil API Python Client.

## Classes

#### BoromirApiClient Class

The `BoromirApiClient` class is the central class in the file. It contains the headers and base URL for API communication. It also initializes the different API endpoints.

```python
class BoromirApiClient:
    def __init__(self, name: str, url: str, version: str, application_key: str, authentication_token: str):
        self.headers = {
            'x-auth-token': authentication_token,
            'x-application-key': application_key,
            'Accept': 'application/json',
            'User-Agent': f'{name} ({url}, {version})'
        }
        self.headers_post = self.headers.copy()
        self.headers_post['Content-type'] = 'application/json'
        self.base_url = 'https://www.worldanvil.com/api/external/boromir/'
        self.article = ArticleCrudEndpoint(self)
        # etc.
```

#### BasicEndpoint Class

This class contains methods for making HTTP requests (`GET`, `PUT`, `PATCH`, `POST`, `DELETE`). These methods are used to interact with the API - fetch, create, update, and delete resources. After making a request, the `_parse_response` function is used to handle the response from the server.

```python
class BasicEndpoint:
    def __init__(self, client: 'AragornApiClient', base_path: str):
        self.client = client
        self.path = base_path
    # etc.
```

#### CrudEndpoint Class

The `CrudEndpoint` class inherits from the `BasicEndpoint` class and provides methods for creating (`PUT`), updating (`PATCH`), and deleting (`DELETE`) resources.

```python
class CrudEndpoint(BasicEndpoint):
    def __init__(self, client: 'AragornApiClient', base_path: str):
        super().__init__(client, base_path)
    # etc.
```

## License

This project is licensed under the terms of the Apache 2.0 License. For complete details, refer to the license [here](http://www.apache.org/licenses/LICENSE-2.0).

Software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

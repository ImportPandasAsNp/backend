
# RecoNN

A cross-platform content recommedation engine, that supports content filtering based on age. It also provides extensive search based from natural language or voice.




## Run Locally

Clone the project

```bash
  git clone https://github.com/ImportPandasAsNp/backend.git
```

Go to the project directory

```bash
  cd backend
```

Setup virtual environment [OPTIONAL]

```bash
  python3 -m venv backend
  source backend/bin/activate
```

Install dependencies

```bash
  pip install requirements.txt
```

Start the server

```bash
  uvicorn app:app --reload
```



## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`PORT` -> port on which server is hosted

`awsAccessKey` -> access key for aws opensearch

`awsSecretKey` -> secret for aws opensearch

`regionName` -> region name for aws opensearch

`domainName` -> domain name for aws opensearch

`jwt_secret` -> secret for JWT based token authentication

`open_ai_api_key` -> OPENAI GPT 3.5 api key





## Demo

https://drive.google.com/file/d/1jVPtFQGy--YQ0nfQAC0WyfWqseWKJU8j/view?usp=sharing


## API Reference

#### Get recommendations for the user

```http
  GET /recommend
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | **Required**. Authorization token |


#### Search based on text

```http
  GET /search?q={text}
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | **Required**. Authorization token |
| `text` | `string` | **Required**. Raw search query from user |

#### Get user watch history

```http
  GET /history
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | **Required**. Authorization token |

#### Update watch history of the user

```http
  PUT /history
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | **Required**. Authorization token |




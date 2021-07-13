import requests
import json
import pathlib

import pytest
from jsonschema import validate, RefResolver

from blog.app import app
from blog.models import Article


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def validate_payload(payload, schema_name):
    """
    Validate payload with selected schema
    """
    schemas_dir = str(
        f'{pathlib.Path(__file__).parent.absolute()}/schemas'
    )
    schema = json.loads(pathlib.Path(f'{schemas_dir}/{schema_name}').read_text())
    validate(
        payload,
        schema,
        resolver=RefResolver(
            'file://' + str(pathlib.Path(f'{schemas_dir}/{schema_name}').absolute()),
            schema  # it's used to resolve file: inside schemas correctly
        )
    )


def test_create_article(client):
    """
    GIVEN request data for new article
    WHEN endpoint /create-article/ is called
    THEN it should return Article in json format matching schema
    """
    data = {
        'author': 'chealsy99@yande.ru',
        'title': 'Test Article #1',
        'content': 'Test content #1'
    }
    response = client.post(
        '/create-article/',
        data=json.dumps(
            data
        ),
        content_type='application/json',
    )

    validate_payload(response.json, 'Article.json')


def test_get_article(client):
    """
    GIVEN ID of article stored in the database
    WHEN endpoint /article/<id-of-article>/ is called
    THEN it should return Article in json format matching schema
    """
    article = Article(
        author='chealsy99@yandex.ru',
        title='Test Article #1',
        content='Test content #1'
    ).save()
    response = client.get(
        f'/article/{article.id}/',
        content_type='application/json',
    )

    validate_payload(response.json, 'Article.json')


def test_list_articles(client):
    """
    GIVEN articles stored in the database
    WHEN endpoint /article-list/ is called
    THEN it should return list of Article in json format matching schema
    """
    Article(
        author='chealsy99@yandex.ru',
        title='Test Article #1',
        content='Test content #1'
    ).save()
    Article(
        author='chealsy99@yandex.ru',
        title='Test Article #2',
        content='Test content #2'
    ).save()
    response = client.get(
        '/article-list/',
        content_type='application/json',
    )

    validate_payload(response.json, 'ArticleList.json')


@pytest.mark.parametrize(
    'data',
    [
        {
            'author': 'Jhon Silver',
            'title': 'Test Article #1',
            'content': 'Test content #1'
        },
        {
            'author': 'Jhon Silver',
            'title': 'Test Article #2'
        },
        {
            'author': 'Jhon Silver',
            'title': None,
            'content': 'Test content #3'
        }
    ]
)
def test_create_article_bad_request(client, data):
    """
    GIVEN request data with invalid values or missing attributes
    WHEN endpoint /create-article/ is called
    THEN it should return status 400 and JSON body
    """
    response = client.post(
        '/create-article/',
        data=json.dumps(
            data
        ),
        content_type='application/json',
    )

    assert response.status_code == 400
    assert response.json is not None


@pytest.mark.e2e
def test_create_list_get(client):
    requests.post(
        'http://localhost:5000/create-article/',
        json={
            'author': 'chealsy99@yandex.ru',
            'title': 'New Article',
            'content': 'Test content'
        }
    )
    response = requests.get(
        'http://localhost:5000/article-list/',
    )

    articles = response.json()

    response = requests.get(
        f'http://localhost:5000/article/{articles[0]["id"]}/',
    )

    assert response.status_code == 200

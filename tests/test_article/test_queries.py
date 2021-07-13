from blog.models import Article
from blog.queries import ListArticlesQuery, GetArticleByIDQuery


def test_list_articles():
    """
    GIVEN 2 articles stored in the database
    WHEN the execute method is called
    THEN it should return 2 articles
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

    query = ListArticlesQuery()

    assert len(query.execute()) == 2


def test_get_article_by_id():
    """
    GIVEN ID of article stored in the database
    WHEN the execute method is called
    THEN it should return the article with the same id
    """
    article = Article(
        author='chealsy99@yandex.ru',
        title='Test Article #1',
        content='Test content #1'
    ).save()

    query = GetArticleByIDQuery(
        id=article.id
    )

    assert query.execute().id == article.id

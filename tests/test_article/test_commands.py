import pytest

from blog.models import Article
from blog.commands import CreateArticleCommand, AlreadyExists


def test_create_article():
    """
    GIVEN CreateArticleCommand with a valid properties author, title and content
    WHEN the execute method is called
    THEN a new Article must exist in the database with the same attributes
    """
    cmd = CreateArticleCommand(
        author='chealsy99@yandex.ru',
        title='Poison Mushrooms',
        content='The most of poison mushroom is Amanita'
    )

    article = cmd.execute()

    db_article = Article.get_by_id(article.id)

    assert db_article.id == article.id
    assert db_article.author == article.author
    assert db_article.title == article.title
    assert db_article.content == article.content


def test_create_article_already_exists():
    """
    GIVEN CreateArticleCommand with a title of some article in database
    WHEN the execute method is called
    THEN the AlreadyExists exception must be raised
    """

    Article(
        author='chealsy99@yandex.ru',
        title='Poison Mushrooms',
        content='It is generally accepted to consider such mushrooms as dangerous: toadstool,'
                ' fly agaric, false mushrooms'
    ).save()

    cmd = CreateArticleCommand(
        author='chealsy99@yandex.ru',
        title='Poison Mushrooms',
        content='It is generally accepted to consider such mushrooms as dangerous: toadstool, fly agaric, '
                'false mushrooms '
    )

    with pytest.raises(AlreadyExists):
        cmd.execute()

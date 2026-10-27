import pytest


def test_homepage_redirects_to_static_html(client):
    # Arrange
    url = "/"

    # Act
    response = client.get(url, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_static_html_contains_activity_and_signup_sections(client):
    # Arrange
    url = "/static/index.html"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assert response.headers["content-type"].split(";")[0] == "text/html"
    assert 'id="activities-list"' in response.text
    assert 'id="signup-form"' in response.text


@pytest.mark.parametrize(
    "filename, content_types",
    [
        ("styles.css", {"text/css"}),
        ("app.js", {"text/javascript", "application/javascript"}),
    ],
)
def test_static_assets_are_served(client, filename, content_types):
    # Arrange
    url = f"/static/{filename}"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assert response.headers["content-type"].split(";")[0] in content_types
    assert response.content


def test_missing_static_asset_returns_not_found(client):
    # Arrange
    url = "/static/nonexistent-asset.js"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

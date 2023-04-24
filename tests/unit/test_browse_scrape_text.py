# Generated by CodiumAI

import requests

from autogpt.commands.web_requests import scrape_text

"""
Code Analysis

Objective:
The objective of the "scrape_text" function is to scrape the text content from
a given URL and return it as a string, after removing any unwanted HTML tags and
 scripts.

Inputs:
- url: a string representing the URL of the webpage to be scraped.

Flow:
1. Send a GET request to the given URL using the requests library and the user agent
 header from the config file.
2. Check if the response contains an HTTP error. If it does, return an error message.
3. Use BeautifulSoup to parse the HTML content of the response and extract all script
 and style tags.
4. Get the text content of the remaining HTML using the get_text() method of
 BeautifulSoup.
5. Split the text into lines and then into chunks, removing any extra whitespace.
6. Join the chunks into a single string with newline characters between them.
7. Return the cleaned text.

Outputs:
- A string representing the cleaned text content of the webpage.

Additional aspects:
- The function uses the requests library and BeautifulSoup to handle the HTTP request
 and HTML parsing, respectively.
- The function removes script and style tags from the HTML to avoid including unwanted
 content in the text output.
- The function uses a generator expression to split the text into lines and chunks,
 which can improve performance for large amounts of text.
"""


class TestScrapeText:
    # Tests that scrape_text() returns the expected text when given a valid URL.
    def test_scrape_text_with_valid_url(self, mocker):
        # Mock the requests.get() method to return a response with expected text
        expected_text = "This is some sample text"
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><body><div><p style='color: blue;'>"
            f"{expected_text}</p></div></body></html>"
        )
        mocker.patch("requests.Session.get", return_value=mock_response)

        # Call the function with a valid URL and assert that it returns the
        #  expected text
        url = "http://www.example.com"
        assert scrape_text(url) == expected_text

    # Tests that the function returns an error message when an invalid or unreachable
    #  url is provided.
    def test_invalid_url(self, mocker):
        # Mock the requests.get() method to raise an exception
        mocker.patch(
            "requests.Session.get", side_effect=requests.exceptions.RequestException
        )

        # Call the function with an invalid URL and assert that it returns an error
        #  message
        url = "http://www.invalidurl.com"
        error_message = scrape_text(url)
        assert "Error:" in error_message

    # Tests that the function returns an empty string when the html page contains no
    #  text to be scraped.
    def test_no_text(self, mocker):
        # Mock the requests.get() method to return a response with no text
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body></body></html>"
        mocker.patch("requests.Session.get", return_value=mock_response)

        # Call the function with a valid URL and assert that it returns an empty string
        url = "http://www.example.com"
        assert scrape_text(url) == ""

    # Tests that the function returns an error message when the response status code is
    #  an http error (>=400).
    def test_http_error(self, mocker):
        # Mock the requests.get() method to return a response with a 404 status code
        mocker.patch("requests.Session.get", return_value=mocker.Mock(status_code=404))

        # Call the function with a URL
        result = scrape_text("https://www.example.com")

        # Check that the function returns an error message
        assert result == "Error: HTTP 404 error"

    # Tests that scrape_text() properly handles HTML tags.
    def test_scrape_text_with_html_tags(self, mocker):
        # Create a mock response object with HTML containing tags
        html = "<html><body><p>This is <b>bold</b> text.</p></body></html>"
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.text = html
        mocker.patch("requests.Session.get", return_value=mock_response)

        # Call the function with a URL
        result = scrape_text("https://www.example.com")

        # Check that the function properly handles HTML tags
        assert result == "This is bold text."

# TomeService

TomeService is a simple, self-hosted web service for managing a library of ebooks. It provides a RESTful API to organize and retrieve information about your books.

## Features

*   **Book Management**: Add, update, delete, and retrieve book information.
*   **Organization**: Organize books by author, series, and tags.
*   **Search**: Search for books by title or author.
*   **File-based**: Book metadata is stored in a simple JSON file, and your ebook files are organized on your filesystem.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.6+
*   pip

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/TomeService.git
    cd TomeService
    ```

2.  **Create and activate a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the environment variables:**

    TomeService uses environment variables to configure the library path and the database file location.

    *   `TOMESERVICE_LIBRARY_PATH`: The path to the directory where your ebook files are stored.
    *   `TOMESERVICE_DB_FILE`: The name of the JSON file that will store your library's metadata. This file will be created inside the `TOMESERVICE_LIBRARY_PATH`.

    You can set these variables in your shell:

    ```bash
    export TOMESERVICE_LIBRARY_PATH="/path/to/your/library"
    export TOMESERVICE_DB_FILE="library.json"
    ```

    Or, you can create a `.env` file in the project root and the application will load them automatically if you have `python-dotenv` installed.

    ```
    TOMESERVICE_LIBRARY_PATH="/path/to/your/library"
    TOMESERVICE_DB_FILE="library.json"
    ```

5.  **Run the application:**

    ```bash
    python server.py
    ```

    The server will start on `http://127.0.0.1:5000`.

## API Endpoints

Here is a summary of the available API endpoints.

### Books

*   **GET /books**
    *   Returns a list of all books.
    *   **Query Parameters**:
        *   `sort_by`: Field to sort by (e.g., `added`, `title`, `author`). Defaults to `added`.
        *   `reverse`: `true` or `false`. Defaults to `true`.
*   **GET /books/<uuid>**
    *   Returns a single book identified by its UUID.
*   **POST /books**
    *   Adds a new book.
    *   **Request Body**: A JSON object representing the book.
        ```json
        {
            "author": "Author Name",
            "title": "Book Title",
            "tags": ["tag1", "tag2"],
            "filename": "book.epub",
            "series": "Series Name",
            "num_series": 1
        }
        ```
*   **PUT /books/<uuid>**
    *   Updates an existing book.
    *   **Request Body**: A JSON object with the fields to update.
*   **DELETE /books/<uuid>**
    *   Deletes a book.

### Tags

*   **GET /tags**
    *   Returns a list of all unique tags.

### Series

*   **GET /series**
    *   Returns a list of all unique series names.

### Authors

*   **GET /authors**
    *   Returns a list of all unique author names.
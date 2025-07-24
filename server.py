from flask import Flask, jsonify, request
from tomeservice.database import LibraryManager
from tomeservice.formvalidators import FormValidators
from tomeservice.filesystem import FileSystemHandler
import os
from pathlib import Path

app = Flask(__name__)

# Configurazione del percorso della libreria e del file di database
# Questi valori dovrebbero essere configurati in modo più robusto, ad esempio tramite variabili d'ambiente o un file di configurazione
LIBRARY_PATH = os.environ.get("TOMESERVICE_LIBRARY_PATH", "../library_data")
DB_FILE = os.environ.get("TOMESERVICE_DB_FILE", "library.json")

# Inizializzazione di LibraryManager
library_manager = LibraryManager(LIBRARY_PATH, DB_FILE)

@app.route('/books', methods=['GET'])
def get_books():
    """Restituisce tutti i libri."""
    sort_by = request.args.get('sort_by', 'added')
    reverse = request.args.get('reverse', 'true').lower() == 'true'
    books = library_manager.books.sort_books(sort_by, reverse)
    return jsonify([book.to_dict() for book in books])

@app.route('/books/<string:uuid>', methods=['GET'])
def get_book(uuid):
    """Restituisce un libro specifico."""
    book = library_manager.books.get_book(uuid)
    if book:
        return jsonify(book.to_dict())
    return jsonify({'error': 'Book not found'}), 404

@app.route('/books', methods=['POST'])
def add_book():
    """Aggiunge un nuovo libro."""
    if not request.json:
        return jsonify({'error': 'Invalid input'}), 400

    data = request.json
    # Qui dovresti aggiungere la validazione dei dati

    # Creazione dell'oggetto Book
    # Nota: questo è un esempio semplificato. Potrebbe essere necessario gestire più campi.
    from tomeservice.database import Book
    from datetime import datetime
    import uuid

    new_book = Book(
        uuid=str(uuid.uuid4()),
        author=data.get('author'),
        title=data.get('title'),
        added=datetime.now(),
        tags=data.get('tags', []),
        filename=data.get('filename', ''),
        series=data.get('series'),
        num_series=data.get('num_series')
    )

    try:
        library_manager.books.add_book(new_book)
        return jsonify(new_book.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/books/<string:uuid>', methods=['PUT'])
def update_book(uuid):
    """Aggiorna un libro esistente."""
    if not request.json:
        return jsonify({'error': 'Invalid input'}), 400

    data = request.json
    try:
        library_manager.books.update_book(uuid, data)
        updated_book = library_manager.books.get_book(uuid)
        return jsonify(updated_book.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/books/<string:uuid>', methods=['DELETE'])
def delete_book(uuid):
    """Elimina un libro."""
    try:
        book = library_manager.books.get_book(uuid)
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        # Opzionale: eliminare il file associato
        # file_path = library_manager.books.get_book_path(book)
        # if os.path.exists(file_path):
        #     os.remove(file_path)

        library_manager.books.remove_book(uuid)
        return jsonify({'message': 'Book deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tags', methods=['GET'])
def get_tags():
    """Restituisce tutti i tag."""
    tags = library_manager.tags.get_all_tag_names()
    return jsonify(tags)

@app.route('/series', methods=['GET'])
def get_series():
    """Restituisce tutti i nomi delle serie."""
    series_names = library_manager.books.get_all_series_names()
    return jsonify(series_names)

@app.route('/authors', methods=['GET'])
def get_authors():
    """Restituisce tutti i nomi degli autori."""
    author_names = library_manager.books.get_all_author_names()
    return jsonify(author_names)

if __name__ == '__main__':
    app.run(debug=True)

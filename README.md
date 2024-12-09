# Path of Exile Forum API

A FastAPI-based REST API that aggregates and serves thread information from various Path of Exile (PoE) official forums. This API automatically fetches and combines threads from multiple forum sections including important announcements, game announcements, development manifestos, and technical news.

## Features

- Asynchronous forum data fetching
- Automatic aggregation of multiple PoE forum sections
- Thread details including titles, URLs, authors, dates, and reply counts
- Sorted results (newest first)
- CORS support enabled
- Health check endpoint
- Interactive API documentation
- Error handling and logging

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/poe-forum-api
cd poe-forum-api
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

1. Start the development server:

```bash
uvicorn main:app --reload
```

2. The server will start at `http://localhost:8000`

### API Endpoints

#### Get Forum Threads

```
GET /api/forum
```

Returns threads from all configured PoE forums.

Example response:

```json
{
  "status": "success",
  "timestamp": "2024-12-09T15:30:45.123456",
  "total_threads": 50,
  "threads": [
    {
      "title": "0.1.0b Patch Notes (restartless)",
      "url": "https://www.pathofexile.com/forum/view-thread/3606561",
      "thread_id": "3606561",
      "author": "Kieren_GGG",
      "post_date": "Dec 9, 2024, 6:11:38 AM",
      "replies": 162
    },
  ]
}
```

#### Health Check

```
GET /api/health
```

Returns the API's current status.

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Monitored Forums

The API currently monitors these official PoE forums:

- Patch Notes Announcements (`/forum/view-forum/2212`)

## Error Handling

The API includes comprehensive error handling:

- Individual forum fetch failures won't cause the entire request to fail
- HTTP errors are properly caught and reported
- Malformed data is handled gracefully

## Development

### Project Structure

```
poe-forum-api/
├── poe2_api.py       # Main application file
├── requirements.txt  # Project dependencies
└── README.md        # Documentation
```

### Adding New Features

To add more forum sections:

1. Open `poe2_api.py`
2. Find the `forums` list in the `get_forum_threads` function
3. Add new forum URLs to the list

## Future Improvements

Planned features:

- Caching system to reduce load on PoE servers
- Pagination for large result sets
- Filtering options (by date, author, etc.)
- Rate limiting
- Authentication system
- Thread content fetching
- Forum-specific endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This API is not officially associated with Path of Exile or Grinding Gear Games. It's a community tool designed to help players access forum information more easily.

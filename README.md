# FastAPI Chat Completion Template

A modern, modular FastAPI template for building chat completion APIs using LangChain and Anthropic's Claude.

## Features

- FastAPI-based REST API
- LangChain integration with Anthropic's Claude
- Modular service architecture
- Async support
- Conversation history management
- Environment-based configuration
- Type hints and validation

## Prerequisites

- Python 3.8+
- Anthropic API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/fastAPI-chat-completion-template.git
cd fastAPI-chat-completion-template
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.EXAMPLE .env
# Edit .env with your Anthropic API key
```

## Project Structure

```
.
├── api/
│   └── routes/
│       └── chat_routes.py    # API endpoints
├── models/
│   └── chat.py              # Pydantic models
├── services/
│   ├── base.py              # Base service class
│   └── chat/
│       ├── base.py          # Base chat service
│       └── anthropic.py     # Anthropic implementation
├── main.py                  # Application entry point
├── requirements.txt         # Project dependencies
└── .env                     # Environment variables
```

## Usage

1. Start the server:

```bash
python -m uvicorn main:app --reload
```

2. Access the API documentation:

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## API Endpoints

### Chat Completion

- `POST /api/chat/completions`
  ```json
  {
    "message": {
      "content": "Your message here",
      "role": "user" // optional, defaults to "user"
    }
  }
  ```

### Chat History

- `GET /api/chat/history` - Get conversation history
- `DELETE /api/chat/history` - Clear conversation history

## Development

### Adding New Chat Providers

1. Create a new service class in `services/chat/`
2. Inherit from `BaseChatService`
3. Implement the `get_chat_response` method
4. Update the service factory in `api/routes/chat_routes.py`

### Running Tests

```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI
- LangChain
- Anthropic

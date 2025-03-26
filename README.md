# FastAPI Project Template

A modern, production-ready template for building APIs with Python 3.8+ using FastAPI. This template provides a modular structure and includes a TODO list CRUD example to demonstrate best practices.

## Features

- 🚀 FastAPI for high-performance API development
- 📁 Modular project structure
- 🔍 Example TODO list CRUD implementation
- 📝 Auto-generated API documentation (Swagger/OpenAPI)
- ✨ Clean, maintainable architecture
- 🔒 Type safety with Pydantic models

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the template:

   ```bash
   git clone https://github.com/yourusername/fastapi-template.git
   cd fastapi-template
   ```

2. Create and activate virtual environment:

   ```bash
   # Create virtual environment
   python -m venv venv

   # Windows
   .\venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python main.py
   ```

5. Open http://localhost:8000/docs to view the API documentation

## Project Structure

fastapi-template/
├── main.py # Application entry point
├── requirements.txt # Project dependencies
├── models/ # Data models
│ └── todo.py # TODO models
└── routes/ # API routes
└── todo_routes.py # TODO endpoints

## API Endpoints

The template includes a complete TODO list API:

- `GET /todos` - List all todos
- `POST /todos` - Create a todo
- `GET /todos/{id}` - Get a specific todo
- `PUT /todos/{id}` - Update a todo
- `DELETE /todos/{id}` - Delete a todo

## Contributing

We welcome contributions! Here's how to contribute to this project:

### Making Changes

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Test your changes
5. Commit with clear messages:
   ```bash
   git commit -m "feat: add new feature"
   ```

### Submitting a Pull Request

1. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Go to the original repository and create a Pull Request
3. Fill in the PR template with:
   - Description of changes
   - Related issue(s)
   - Testing performed
   - Screenshots (if applicable)

### Pull Request Guidelines

- Follow existing code style
- Add tests for new features
- Update documentation
- One feature per PR
- Keep PRs focused and manageable in size

## Development

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions and classes
- Keep functions focused and single-purpose

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Getting Help

- Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
- Open an issue for bugs
- Start a discussion for questions

# Contributing to Overfitting Demo

Thank you for your interest in contributing! This is primarily a portfolio project, but improvements and suggestions are welcome.

## How to Contribute

1. **Fork the Repository**
   - Click the "Fork" button at the top right of the repository page

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/your-username/overfitting-demo.git
   cd overfitting-demo
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed

5. **Run Tests**
   ```bash
   pytest
   black src/ scripts/ tests/
   flake8 src/ scripts/ tests/
   ```

6. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add feature: description of your feature"
   ```

7. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Describe your changes

## Code Style

- **Python**: Follow PEP 8
- **Line Length**: 100 characters max
- **Formatter**: Black
- **Linter**: Flake8, Pylint
- **Type Hints**: Use where appropriate
- **Docstrings**: Google style

## Testing

- Write tests for all new features
- Maintain 80%+ code coverage
- Use pytest for testing
- Add tests in `tests/` folder

## Documentation

- Update README.md if needed
- Add docstrings to functions
- Update architecture docs for major changes
- Keep configuration files current

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Questions about the code
- Suggestions for improvements

Thank you for contributing! 🎉

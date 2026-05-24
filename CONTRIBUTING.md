# Contributing to Thyroid Nodule Detection Project

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and constructive in all interactions
- Provide helpful feedback and support to other contributors
- Report any unacceptable behavior to the project maintainers

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/ThyroidNoduleProject.git
   cd ThyroidNoduleProject
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Making Changes

1. **Code style**: Follow PEP 8 for Python code
2. **Comments**: Add docstrings to functions and classes
3. **Testing**: Write tests for new features
4. **Documentation**: Update README.md or relevant docs

### Testing Your Changes

```bash
# Run inference tests
python inference.py test_image.jpg

# Test API endpoints
python launch.py
# Visit http://localhost:5000 in your browser

# Test authentication
pytest test_auth.py
```

### Commit Guidelines

- Write clear, descriptive commit messages
- Use present tense ("Add feature" not "Added feature")
- Reference issues when relevant: "Fixes #123"
- Example:
  ```
  git commit -m "Add CUDA memory optimization for batch processing"
  ```

## Types of Contributions

### Bug Reports

If you find a bug, please:
1. Check if it's already reported in [Issues](https://github.com/yourusername/ThyroidNoduleProject/issues)
2. Create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Relevant error logs

### Feature Requests

For new features:
1. Check existing issues first
2. Create an issue describing:
   - What problem it solves
   - Proposed implementation
   - Any examples or mock-ups
3. Wait for feedback before implementing

### Pull Requests

1. **Before starting**: Discuss major changes in an issue first
2. **Commit messages**: Write clear, atomic commits
3. **Testing**: Test locally before pushing
4. **Documentation**: Update docs and comments
5. **PR description**: Explain what and why

**PR Checklist**:
- [ ] Tested locally
- [ ] Updated documentation
- [ ] Followed code style
- [ ] No unrelated changes
- [ ] Clear commit messages

## Important Areas for Contribution

### High Priority
- [ ] Model optimization and inference speed
- [ ] Accuracy improvements
- [ ] API documentation
- [ ] Bug fixes

### Medium Priority
- [ ] Frontend UI improvements
- [ ] Additional datasets support
- [ ] Performance monitoring
- [ ] Deployment guides

### Nice to Have
- [ ] Docker support
- [ ] Kubernetes deployment
- [ ] Mobile app
- [ ] Additional model architectures

## Documentation

When contributing, please update:
- **README.md** - For new features
- **API Documentation** - For endpoint changes
- **Code comments** - For complex logic
- **CHANGELOG** - For all changes

## Review Process

1. **Automated checks**: GitHub Actions runs tests
2. **Code review**: Maintainers review your code
3. **Feedback**: Address review comments
4. **Merge**: After approval, your PR is merged

## Development Setup

### Tools Recommended
- **IDE**: Visual Studio Code or PyCharm
- **Python**: 3.8 or higher
- **Git**: Latest version
- **Docker**: For containerized testing (optional)

### Useful Commands

```bash
# Check code style
flake8 backend/

# Format code
black backend/

# Run tests
pytest tests/

# Build documentation
python -m pip install sphinx
cd docs && make html
```

## Questions?

- **Documentation**: Check [README.md](README.md) and existing docs
- **Issues**: Search [GitHub Issues](https://github.com/yourusername/ThyroidNoduleProject/issues)
- **Discussions**: Start a [Discussion](https://github.com/yourusername/ThyroidNoduleProject/discussions)

## Recognition

Contributors will be recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md) file
- Release notes
- Project documentation

Thank you for contributing! 🙏

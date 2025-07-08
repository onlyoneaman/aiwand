# Contributing to AIWand

Thank you for your interest in contributing to AIWand! This guide serves as a comprehensive reference for both AI assistants and human contributors to ensure consistency, quality, and maintainability.

## 🎯 Core Principles

- **Package-First Approach**: AIWand is primarily a Python package; CLI is secondary
- **Documentation Accuracy**: Code and docs must always match
- **Single Source of Truth**: Version in `src/aiwand/__init__.py` only
- **Smart Defaults**: Sensible defaults with optional customization
- **Type Safety**: Full type hints and validation
- **User Experience**: Clear error messages and helpful feedback

## 📋 Before Contributing

### Prerequisites
- Python 3.8+
- Git
- Understanding of Python packaging (src/ layout)
- Familiarity with OpenAI and Gemini APIs

### Development Setup
```bash
# Clone the repository
git clone https://github.com/onlyoneaman/aiwand.git
cd aiwand

# Set up development environment
./scripts/setup-dev.sh        # Linux/Mac
# or
scripts\setup-dev.bat         # Windows

# Verify installation
python test_install.py
python examples/basic_usage.py
```

## 🏗️ Project Structure

```
aiwand/
├── src/aiwand/              # Main package (src layout)
│   ├── __init__.py          # VERSION (single source of truth)
│   ├── config.py            # API configuration & provider selection
│   ├── core.py              # Core AI functionality
│   ├── cli.py               # Command line interface
│   └── helper.py            # Utility functions
├── docs/                    # Documentation
├── scripts/                 # Automation scripts
├── examples/                # Usage examples
└── CHANGELOG.md             # Release history
```

## 🔧 Development Workflow

### 1. Making Changes

#### For New Features
1. **Check existing functionality** - Avoid duplication
2. **Update relevant modules**:
   - Add functions to appropriate module (`core.py`, `helper.py`, etc.)
   - Export in `src/aiwand/__init__.py` if public API
   - Add CLI commands in `cli.py` if applicable
3. **Follow code standards** (see below)
4. **Add comprehensive tests**

#### For Bug Fixes
1. **Identify root cause** before implementing fix
2. **Maintain backward compatibility** when possible
3. **Add defensive programming** to prevent similar issues
4. **Test with both API providers** (OpenAI and Gemini)

#### For Documentation Updates
1. **Verify accuracy** against actual code
2. **Update all relevant files**:
   - README.md for overview changes
   - docs/ for detailed documentation
   - examples/ for usage demonstrations
3. **Check for broken links** and outdated information

### 2. Code Standards

#### Python Code Style
```python
# Type hints are mandatory
def function_name(param1: str, param2: Optional[int] = None) -> Dict[str, Any]:
    """Brief description of what the function does.
    
    Args:
        param1: Description of first parameter
        param2: Description of optional parameter
        
    Returns:
        Dictionary containing the result data
        
    Raises:
        ValueError: When param1 is invalid
        AIError: When external API call fails
    """
    # Implementation here
    pass
```

#### Required Standards
- **PEP 8 compliant** formatting
- **Type hints** for all function parameters and return values
- **Google-style docstrings** for all public functions
- **Comprehensive error handling** with user-friendly messages
- **Descriptive variable names** (snake_case)

#### Error Handling Pattern
```python
try:
    result = some_operation()
    return result
except AIError as e:
    raise AIError(str(e))  # Re-raise AI-specific errors
except ValueError as e:
    raise ValueError(f"Invalid input: {str(e)}")
except Exception as e:
    raise Exception(f"Operation failed: {str(e)}")
```

### 3. API Design Guidelines

#### Public API Functions
- **Consistent naming**: Use clear, descriptive names
- **Smart defaults**: Provide sensible default values
- **Optional parameters**: Use keyword arguments for optional features
- **Provider agnostic**: Work with both OpenAI and Gemini
- **Type validation**: Validate inputs and provide clear error messages

#### Configuration Pattern
```python
# Always use the configuration system
client = get_ai_client()
model = get_model_name()

# Never hardcode API keys or model names
```

### 4. CLI Integration

When adding new functions to the package:

1. **Evaluate CLI necessity**: Not all functions need CLI equivalents
2. **Follow existing patterns**: Use subcommands under appropriate groups
3. **Add help text**: Comprehensive help for all commands and options
4. **Support batch operations**: Use `--count` for multiple outputs when applicable
5. **Error handling**: Consistent error messages and exit codes

#### CLI Command Pattern
```python
# In cli.py
parser = subparsers.add_parser('command', help='Command description')
parser.add_argument('arg', help='Argument description')
parser.add_argument('--option', default=value, help='Option description')

# Implementation
if args.command == 'command':
    try:
        result = package_function(args.arg, option=args.option)
        print(result)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
```

## 📝 Documentation Standards

### Always Update Together
- **API changes** → Update `docs/api-reference.md`
- **CLI changes** → Update `docs/cli.md`
- **New features** → Update README.md examples
- **Version changes** → Update CHANGELOG.md

### Documentation Requirements
- **Complete function documentation** in API reference
- **Usage examples** for all public functions
- **CLI help consistency** with documentation
- **Error scenarios** documented with solutions

### Example Documentation Pattern
```markdown
### `function_name(param1, param2=None)`

Brief description of the function.

**Parameters:**
- `param1` (str): Description of required parameter
- `param2` (int, optional): Description of optional parameter

**Returns:** Description of return value

**Raises:**
- `ValueError`: When validation fails
- `AIError`: When API call fails

**Example:**
```python
import aiwand
result = aiwand.function_name("value", param2=42)
```
```

## 🔄 Version Management

### Version Bump Process
```bash
# Patch version (default)
python scripts/bump-version.py        # 0.3.1 -> 0.3.2

# Specific version type
python scripts/bump-version.py minor  # 0.3.1 -> 0.4.0
python scripts/bump-version.py major  # 0.3.1 -> 1.0.0
```

### Changelog Requirements
For every version bump, update `CHANGELOG.md`:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- **Feature Name**: Description of new functionality
- **API Enhancement**: Description of API improvements

### Changed
- **Breaking Change**: Description with migration guide
- **Improvement**: Description of enhancements

### Fixed
- **Bug Fix**: Description of issue and resolution

### Technical Improvements
- Technical details for developers
```

## 🚀 Publishing Workflow

### Pre-Publication Checklist
- [ ] All tests pass (`python test_install.py`)
- [ ] Documentation is updated and accurate
- [ ] Examples work correctly
- [ ] CHANGELOG.md is updated
- [ ] Version is bumped appropriately
- [ ] No sensitive information in code
- [ ] All changes are committed

### Publishing Process
```bash
# Automated publishing (recommended)
python scripts/publish.py

# The script will:
# 1. Verify git status is clean
# 2. Run installation tests
# 3. Build the package
# 4. Upload to PyPI
# 5. Create git tag
# 6. Push to GitHub
```

## 🤖 AI Assistant Guidelines

### When Adding Features
1. **Understand the request** fully before implementing
2. **Check existing functionality** to avoid duplication
3. **Follow established patterns** in the codebase
4. **Implement complete solutions**:
   - Core function in appropriate module
   - Export in `__init__.py` if public
   - CLI command if applicable
   - Comprehensive documentation
   - Usage examples
5. **Test thoroughly** before suggesting changes

### Code Quality Checklist
- [ ] Type hints on all function signatures
- [ ] Comprehensive docstrings with examples
- [ ] Error handling with user-friendly messages
- [ ] Consistent with existing code style
- [ ] No hardcoded values (use configuration)
- [ ] Works with both OpenAI and Gemini

### Documentation Requirements
- [ ] API reference updated
- [ ] CLI reference updated (if applicable)
- [ ] README examples updated
- [ ] CHANGELOG.md entry added
- [ ] Examples work and are tested

### Testing Requirements
- [ ] Functions work as documented
- [ ] Error handling works correctly
- [ ] CLI commands function properly
- [ ] Examples run without errors
- [ ] Both API providers supported

## 🛠️ Common Tasks

### Adding a New Helper Function
1. **Implement in `src/aiwand/helper.py`**
2. **Export in `src/aiwand/__init__.py`**
3. **Add CLI command in `src/aiwand/cli.py`**
4. **Update documentation**:
   - `docs/api-reference.md`
   - `docs/cli.md`
   - README examples
5. **Update `examples/helper_usage.py`**
6. **Test everything**

### Adding a New Core AI Function
1. **Implement in `src/aiwand/core.py`**
2. **Use configuration system** (`get_ai_client()`, `get_model_name()`)
3. **Export in `src/aiwand/__init__.py`**
4. **Add CLI command if applicable**
5. **Update all documentation**
6. **Add to `examples/basic_usage.py`**

### Modifying Existing Functionality
1. **Maintain backward compatibility**
2. **Update all related documentation**
3. **Test with existing examples**
4. **Consider deprecation** for major changes
5. **Update changelog** appropriately

## 🔍 Quality Assurance

### Before Submitting Changes
```bash
# Run tests
python test_install.py

# Test examples
python examples/basic_usage.py
python examples/helper_usage.py

# Test CLI
aiwand --help
aiwand helper --help
aiwand status

# Check documentation consistency
# Verify all examples in docs work
```

### Code Review Checklist
- [ ] Code follows established patterns
- [ ] Documentation is complete and accurate
- [ ] Error handling is comprehensive
- [ ] No breaking changes without justification
- [ ] Performance impact considered
- [ ] Security implications reviewed

## 🚨 Common Pitfalls to Avoid

### ❌ Don't Do This
```python
# Hardcoded API keys
client = OpenAI(api_key="sk-...")

# Missing type hints
def function(text):

# No error handling
result = api_call()

# Undocumented functions
def mystery_function(x, y):
    return x + y
```

### ✅ Do This Instead
```python
# Use configuration system
client = get_ai_client()

# Complete type hints
def function(text: str) -> str:

# Comprehensive error handling
try:
    result = api_call()
except Exception as e:
    raise AIError(f"API call failed: {e}")

# Well-documented functions
def add_numbers(x: int, y: int) -> int:
    """Add two numbers together.
    
    Args:
        x: First number
        y: Second number
        
    Returns:
        Sum of x and y
    """
    return x + y
```

## 📞 Getting Help

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Documentation**: Check the `docs/` directory for detailed guides
- **Examples**: Look at `examples/` for usage patterns

## 📄 License

By contributing to AIWand, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to AIWand!** 🪄

Your contributions help make AI-powered text processing accessible and reliable for developers worldwide. 
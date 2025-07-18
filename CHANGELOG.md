# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.2] - 2025-01-27

### Enhanced
- **Improved System Prompt Handling**: Enhanced `make_ai_request` function for better system prompt control
  - Empty string system prompts (`""`) are now respected instead of using default
  - Prevents duplicate system messages when messages already contain a system message
  - Made `messages` parameter optional - can now use `system_prompt` alone for simple generation
  - Added automatic user message when only system prompt is provided
  - Better handling of edge cases in conversation building

### Added
- **New Test Examples**: Comprehensive test scripts for system prompt functionality
  - `examples/test_system_prompt.py` - Full test suite with all scenarios
  - `examples/simple_system_prompt_test.py` - Quick verification tests
  - Real-world examples like Bhagavad Gita chat implementation

### Documentation
- **Updated API Reference**: Enhanced documentation for `make_ai_request` with new capabilities
  - Added examples for system-prompt-only usage
  - Documented new optional messages parameter behavior
  - Added comprehensive usage patterns for different scenarios

## [0.4.1] - 2025-01-27

### Added
- **Advanced API Access**: Exposed `make_ai_request` function for direct AI requests
  - Full access to unified AI request system with provider switching
  - Built-in response format handling for structured output (JSON)
  - Custom system prompt support with sensible defaults
  - Complete conversation history management
- **Enhanced System Prompts**: Function-specific system prompts for better AI behavior
  - Specialized prompts for summarization, chat, and text generation
  - Default system prompt for consistent AIWand identity
  - Improved response quality and task-specific optimization
- **New Utility Functions**: Additional configuration and inspection utilities
  - `get_ai_client()` - Get configured AI client for current provider
  - `get_current_provider()` - Check currently active provider
  - `get_model_name()` - Get current model name from preferences
  - `DEFAULT_SYSTEM_PROMPT` - Access to default system prompt constant
- **Comprehensive Examples**: New example file `examples/direct_ai_request.py`
  - Demonstrates advanced `make_ai_request` usage patterns
  - Shows structured output, conversation handling, and model selection
  - Includes best practices for different use cases

### Changed
- **Core Functions**: Updated to use specialized system prompts for better results
- **API Documentation**: Enhanced with advanced functions and comprehensive examples
- **Package Exports**: Organized exports with clear categories (core, config, types, helpers)

## [0.4.0] - 2025-01-27

### Added
- **Latest AI Models**: Support for newest OpenAI and Gemini models
  - OpenAI: `o3`, `o3-mini`, `o1`, `o1-mini`, `gpt-4.1`, `gpt-4.1-mini`
  - Gemini: `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`, `gemini-2.0-pro`

### Changed
- **Default Models**: Updated to `gpt-4o` (OpenAI) and `gemini-2.0-flash` (Gemini)
- **Documentation**: Updated API reference and CLI docs with latest models

## [0.3.2] - 2025-01-27

### Added
- **Helper Functions**: New utility functions for development and testing
  - `generate_random_number(length=6)` - Generate random numbers with configurable digit length
  - `generate_uuid(version=4, uppercase=False)` - Generate UUIDs (version 1 or 4) with formatting options
- **CLI Helper Commands**: New command-line interface for helper functions
  - `aiwand helper random` - Generate random numbers with `--length` and `--count` options
  - `aiwand helper uuid` - Generate UUIDs with `--version`, `--uppercase`, and `--count` options
- **Enhanced Examples**: Updated `examples/helper_usage.py` with comprehensive helper function demonstrations
- **API Documentation**: Complete documentation for new helper functions in API reference
- **CLI Documentation**: Enhanced CLI reference with helper command examples and usage patterns

### Changed
- **Package Exports**: Added helper functions to public API (`aiwand.generate_random_number`, `aiwand.generate_uuid`)
- **README**: Updated features list and usage examples to showcase helper utilities and CLI commands
- **Documentation**: Enhanced API reference with helper function section and CLI usage patterns
- **CLI Description**: Updated helper command description to emphasize development and testing utilities

### Technical Improvements
- Type-safe random number generation with exact digit length control
- Support for both UUID1 (timestamp-based) and UUID4 (random) generation
- Comprehensive error handling and validation for helper functions
- Added helper utilities to package's `__all__` exports
- CLI integration with batch generation support (multiple numbers/UUIDs)
- Perfect for shell scripting and automation workflows

## [0.3.1] - 2025-01-27

### Fixed
- **Documentation Accuracy**: Removed non-existent `configure_api_key()` function from all documentation
- **API Reference**: Corrected configuration approach to use environment variables and `setup_user_preferences()`
- **Model Names**: Updated supported model lists to match actual implementation
- **Installation Guide**: Fixed programmatic setup examples to show correct methods
- **Package Focus**: Prioritized Python package usage over CLI in documentation

### Changed
- **API Exports**: Removed unrelated Chrome helper functions (`find_chrome_binary`, `get_chrome_version`) from public API
- **Documentation Structure**: Reorganized README to emphasize package-first usage
- **Error Handling**: Enhanced documentation with proper `AIError` exception examples

### Technical Improvements
- Cleaned up package exports to focus on core AI functionality
- Improved documentation consistency across all files
- Better error handling examples and best practices

## [0.3.0] - 2025-06-23

### Added
- **Direct Prompt Support**: New simplified CLI usage - `aiwand "Your prompt here"` for instant AI chat
- **Enhanced CLI Experience**: Direct prompts bypass subcommands for faster interaction
- **Updated Documentation**: Added quick start examples and direct prompt usage guide
- **Backward Compatibility**: All existing subcommands (chat, summarize, generate) continue to work

### Changed
- **CLI Help Text**: Updated to showcase direct prompt feature as primary usage method
- **README Examples**: Prioritized direct prompt usage in documentation
- **CLI Reference**: Added comprehensive direct prompt examples and use cases

### Technical Improvements
- Smart command detection that differentiates between subcommands and direct prompts
- Maintained full backward compatibility with existing CLI structure
- Enhanced argument parsing with better help formatting

## [0.2.0] - 2025-06-23

### Added
- **Interactive Setup System**: New `aiwand setup` command for guided configuration
- **User Preferences**: Persistent configuration storage in `~/.aiwand/config.json`
- **Enhanced Model Support**: Added GPT-4o, GPT-4o-mini, Gemini 2.0 Flash Experimental models
- **Configuration Status Command**: New `aiwand status` to display current settings
- **Smart Provider Selection**: Hierarchical preference system (user config → env vars → auto-detection)
- **Per-Provider Model Selection**: Configure different models for each AI provider
- **AIError Exception Class**: Better error handling with specific error types

### Changed
- **Completely Rewritten Configuration System**: More robust and user-friendly
- **Updated CLI Interface**: Removed old config command, added setup/status commands
- **Enhanced Examples**: Updated to showcase new setup system and preferences
- **Improved Test Suite**: Tests now cover new API functions and error handling
- **Better Error Messages**: More helpful guidance for setup and configuration

### Technical Improvements
- Centralized configuration management with fallback logic
- Support for multiple model options per provider
- Persistent user preference storage
- Enhanced type hints and error handling
- Improved CLI argument parsing and help messages

## [0.1.0] - 2025-06-23

### Added
- Centralized version management (single source of truth in `__init__.py`)
- Comprehensive documentation structure in `docs/` directory
- Professional README with badges and social links  
- X (Twitter) profile integration (@onlyoneaman)
- Detailed installation guide with troubleshooting
- Complete API reference documentation
- CLI reference with examples
- Virtual environment best practices guide

### Changed
- Updated contact email to 2000.aman.sinha@gmail.com
- Streamlined README from 308 to 106 lines (65% reduction)
- Reorganized documentation into modular structure
- Improved package metadata and descriptions

### Fixed
- Improved error handling and validation
- Enhanced setup scripts for development environment

## [0.0.1] - 2025-06-23

### Added
- Initial release of AIWand
- Smart AI provider selection (OpenAI & Gemini APIs)
- Text summarization with multiple styles (concise, detailed, bullet-points)
- AI chat functionality with conversation history support
- Text generation with customizable parameters
- Command line interface (CLI) with auto-model selection
- Virtual environment support with automated setup scripts
- Environment-based configuration with `.env` file support
- Smart model selection based on available API keys
- Support for both OpenAI and Google Gemini models
- Comprehensive error handling and input validation
- MIT License
- PyPI package distribution
- GitHub repository with complete documentation

### Technical Features
- Python 3.8+ compatibility
- Type hints throughout codebase
- Modular architecture with separate config, core, and CLI modules
- Automated development environment setup (Linux/Mac/Windows)
- Professional package structure with src/ layout
- Comprehensive test suite and installation verification 
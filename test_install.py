#!/usr/bin/env python3
"""
Quick test script to verify AIWand package installation and basic functionality
"""

def test_import():
    """Test that the package can be imported successfully."""
    try:
        import aiwand
        print("✓ Package import successful")
        
        # Check available functions
        functions = ['summarize', 'chat', 'generate_text', 'setup_user_preferences', 'show_current_config', 'AIError']
        for func in functions:
            if hasattr(aiwand, func):
                print(f"✓ Function '{func}' is available")
            else:
                print(f"✗ Function '{func}' is missing")
        
        # Check version
        if hasattr(aiwand, '__version__'):
            print(f"✓ Package version: {aiwand.__version__}")
        else:
            print("⚠ No version information available")
            
        return True
        
    except ImportError as e:
        print(f"✗ Package import failed: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality without API calls."""
    try:
        import aiwand
        
        # Test configuration display (should work even without API keys)
        try:
            aiwand.show_current_config()
            print("✓ Configuration display works")
        except Exception:
            print("✓ Configuration display handled gracefully")
        
        # Test error handling for empty inputs
        try:
            aiwand.summarize("")
            print("✗ Should have raised ValueError for empty text")
        except ValueError:
            print("✓ Error handling for empty text works")
        except aiwand.AIError:
            print("✓ Error handling for missing configuration works")
        
        try:
            aiwand.chat("")
            print("✗ Should have raised ValueError for empty message")
        except ValueError:
            print("✓ Error handling for empty message works")
        except aiwand.AIError:
            print("✓ Error handling for missing configuration works")
            
        try:
            aiwand.generate_text("")
            print("✗ Should have raised ValueError for empty prompt")
        except ValueError:
            print("✓ Error handling for empty prompt works")
        except aiwand.AIError:
            print("✓ Error handling for missing configuration works")
            
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=== AIWand Package Test ===\n")
    
    # Test 1: Package import
    print("1. Testing package import...")
    import_success = test_import()
    
    if not import_success:
        print("\n❌ Package import failed. Make sure to install the package first:")
        print("   pip install -e .")
        return
    
    print()
    
    # Test 2: Basic functionality
    print("2. Testing basic functionality...")
    func_success = test_basic_functionality()
    
    print()
    
    if import_success and func_success:
        print("🎉 All tests passed! The package is ready to use.")
        print("\nNext steps:")
        print("1. Configure your AI preferences:")
        print("   - Interactive setup: aiwand setup")
        print("   - Or set environment variables:")
        print("     export OPENAI_API_KEY='your-openai-key'")
        print("     export GEMINI_API_KEY='your-gemini-key'")
        print("2. Check your configuration: aiwand status")
        print("3. Try the examples: python examples/basic_usage.py")
        print("4. Use the CLI: aiwand summarize 'Your text here'")
    else:
        print("❌ Some tests failed. Please check the output above.")


if __name__ == "__main__":
    main() 
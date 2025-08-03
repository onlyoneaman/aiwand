#!/usr/bin/env python3
"""
Test OCR functionality with receipt image.

This example demonstrates the new OCR capabilities in AIWand,
extracting text from images and using it as context for AI processing.
"""

import os
import sys
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dotenv import load_dotenv
from aiwand.config import call_ai, _extract_text_using_ocr

load_dotenv()

# Receipt image URL for testing
RECEIPT_IMAGE_URL = "https://bella.amankumar.ai/examples/receipt_1.jpeg"

# Expected words/phrases to test OCR accuracy
EXPECTED_WORDS = [
    "Liquor Street",
    "ODVJH Private Limited", 
    "Faridabad",
    "Tandoori chicken",
    "Lasooni Dal Tadka",
    "HYDERABADI MURG",
    "BIRYANI",
    "Total:",
    "1,139.00",
    "CGST",
    "SGST"
]

def test_ocr_basic():
    """Test basic OCR functionality - extract text from receipt image."""
    print("🔍 Testing OCR text extraction...")
    
    try:
        # Use OCR to extract text from the receipt
        extracted_text = _extract_text_using_ocr(
            images=[RECEIPT_IMAGE_URL],
            model="gemini-2.0-flash-lite"
        )
        
        print("✅ OCR extraction successful!")
        print("\n--- EXTRACTED TEXT ---")
        print(extracted_text)
        print("--- END EXTRACTED TEXT ---\n")
        
        return extracted_text
        
    except Exception as e:
        print(f"❌ OCR extraction failed: {e}")
        return None

def test_ocr_accuracy(extracted_text):
    """Test OCR accuracy by checking for expected words."""
    if not extracted_text:
        print("❌ Cannot test accuracy - no extracted text")
        return False
        
    print("🎯 Testing OCR accuracy...")
    
    found_words = []
    missing_words = []
    
    extracted_lower = extracted_text.lower()
    
    for word in EXPECTED_WORDS:
        if word.lower() in extracted_lower:
            found_words.append(word)
        else:
            missing_words.append(word)
    
    accuracy = (len(found_words) / len(EXPECTED_WORDS)) * 100
    
    print(f"📊 OCR Accuracy: {accuracy:.1f}% ({len(found_words)}/{len(EXPECTED_WORDS)} words found)")
    print(f"✅ Found words: {', '.join(found_words)}")
    
    if missing_words:
        print(f"❌ Missing words: {', '.join(missing_words)}")
    
    return accuracy >= 70  # Consider 70%+ accuracy as success

def test_ocr_with_analysis():
    """Test OCR combined with AI analysis."""
    print("🤖 Testing OCR + AI analysis...")
    
    try:
        # Use OCR to extract text and then analyze it
        analysis = call_ai(
            user_prompt="Analyze this receipt and provide a summary of the order, total amount, and restaurant details.",
            images=[RECEIPT_IMAGE_URL],
            use_ocr=True,
            use_vision=True  # Use both OCR text and raw image for best results
        )
        
        print("✅ OCR + Analysis successful!")
        print("\n--- AI ANALYSIS ---")
        print(analysis)
        print("--- END ANALYSIS ---\n")
        
        return True
        
    except Exception as e:
        print(f"❌ OCR + Analysis failed: {e}")
        return False

def test_multiple_images_ocr():
    """Test OCR with multiple images (using same image twice to simulate multiple)."""
    print("📊 Testing OCR with multiple images...")
    
    try:
        # Test with multiple images - use the same receipt twice to simulate multiple images
        extracted_text = call_ai(
            user_prompt="Extract all text from these images:",
            images=[RECEIPT_IMAGE_URL, RECEIPT_IMAGE_URL],  # Duplicate for testing
            use_ocr=True,
            use_vision=False
        )
        
        print("✅ Multiple images OCR successful!")
        print("\n--- EXTRACTED TEXT FROM MULTIPLE IMAGES ---")
        print(extracted_text)
        print("--- END EXTRACTED TEXT ---\n")
        
        # Check if the text contains image separators
        has_separators = "=== IMAGE" in extracted_text
        print(f"📋 Image separation detected: {'✅ YES' if has_separators else '❌ NO'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Multiple images OCR failed: {e}")
        return False

def test_comparison_no_ocr():
    """Test the same analysis without OCR for comparison."""
    print("🔄 Testing analysis without OCR (for comparison)...")
    
    try:
        # Use direct vision without OCR
        analysis = call_ai(
            user_prompt="Analyze this receipt and provide a summary of the order, total amount, and restaurant details.",
            images=[RECEIPT_IMAGE_URL],
            use_ocr=False,
            use_vision=True,
            model="gemini-2.5-flash-lite"
        )
        
        print("✅ Direct vision analysis successful!")
        print("\n--- DIRECT VISION ANALYSIS ---")
        print(analysis)
        print("--- END ANALYSIS ---\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct vision analysis failed: {e}")
        return False

def main():
    """Run all OCR tests."""
    print("🧪 AIWand OCR Test Suite")
    print("=" * 50)
    
    # Test 1: Basic OCR extraction
    extracted_text = test_ocr_basic()
    
    # Test 2: Accuracy check
    if extracted_text:
        accuracy_passed = test_ocr_accuracy(extracted_text)
    else:
        accuracy_passed = False
    
    # Test 3: OCR + AI analysis
    analysis_passed = test_ocr_with_analysis()
    
    # Test 4: Multiple images OCR
    multiple_images_passed = test_multiple_images_ocr()
    
    # Test 5: Comparison without OCR
    comparison_passed = test_comparison_no_ocr()
    
    # Summary
    print("📋 TEST SUMMARY")
    print("=" * 50)
    print(f"OCR Extraction:     {'✅ PASSED' if extracted_text else '❌ FAILED'}")
    print(f"OCR Accuracy:       {'✅ PASSED' if accuracy_passed else '❌ FAILED'}")
    print(f"OCR + Analysis:     {'✅ PASSED' if analysis_passed else '❌ FAILED'}")
    print(f"Multiple Images:    {'✅ PASSED' if multiple_images_passed else '❌ FAILED'}")
    print(f"Direct Vision:      {'✅ PASSED' if comparison_passed else '❌ FAILED'}")
    
    all_passed = all([extracted_text, accuracy_passed, analysis_passed, multiple_images_passed, comparison_passed])
    print(f"\nOverall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
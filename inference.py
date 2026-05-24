#!/usr/bin/env python3
"""
Inference Script - Test Model on Single Images or Image Directory
Usage:
  python inference.py image.jpg
  python inference.py image_folder/
"""

import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import numpy as np
from pathlib import Path
import sys
import os

CONFIG = {
    "model_path": "checkpoints/best_model_ultrasafe.pt",
    "device": "cuda" if torch.cuda.is_available() else "cpu",
    "class_names": ["Benign", "Malignant"],
    "threshold": 0.78,  # Optimal threshold (was 0.5) - improves balanced accuracy
}

# ============================================================================
# LOAD MODEL
# ============================================================================

def load_model():
    """Load trained ResNet50 model"""
    device = torch.device(CONFIG['device'])
    model = models.resnet50(pretrained=True)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 2)
    
    try:
        model.load_state_dict(torch.load(CONFIG['model_path'], map_location=device))
        model = model.to(device)
        model.eval()
        print(f"✅ Model loaded successfully")
        return model, device
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        sys.exit(1)

# ============================================================================
# PREPROCESSING
# ============================================================================

def get_transforms():
    """Get image preprocessing transforms"""
    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

# ============================================================================
# INFERENCE
# ============================================================================

def predict_image(image_path, model, device, transforms):
    """Predict class for a single image"""
    try:
        # Load and preprocess image
        image = Image.open(image_path).convert('RGB')
        image_tensor = transforms(image).unsqueeze(0).to(device)
        
        # Predict
        with torch.no_grad():
            outputs = model(image_tensor)
            confidences = torch.softmax(outputs, dim=1)[0]
            # Use threshold instead of argmax
            # If P(malignant) >= threshold -> malignant (1), else benign (0)
            malignant_prob = confidences[1].item()
            prediction = 1 if malignant_prob >= CONFIG['threshold'] else 0
        
        return {
            "path": str(image_path),
            "prediction": CONFIG['class_names'][prediction],
            "confidence": confidences[prediction].item(),
            "benign_score": confidences[0].item(),
            "malignant_score": confidences[1].item(),
            "error": None
        }
    
    except Exception as e:
        return {
            "path": str(image_path),
            "prediction": "ERROR",
            "confidence": 0.0,
            "benign_score": 0.0,
            "malignant_score": 0.0,
            "error": str(e)
        }

# ============================================================================
# BATCH INFERENCE
# ============================================================================

def predict_directory(directory, model, device, transforms):
    """Predict for all images in a directory"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    image_files = [f for f in Path(directory).glob('*') 
                   if f.suffix.lower() in image_extensions]
    
    if not image_files:
        print(f"⚠️  No images found in {directory}")
        return []
    
    print(f"Found {len(image_files)} images. Processing...")
    results = []
    
    for idx, image_path in enumerate(image_files, 1):
        result = predict_image(image_path, model, device, transforms)
        results.append(result)
        
        # Display result
        if result['error']:
            print(f"[{idx}/{len(image_files)}] ❌ {image_path.name}: {result['error']}")
        else:
            conf_color = "🟢" if result['confidence'] > 0.8 else "🟡" if result['confidence'] > 0.6 else "🔴"
            print(f"[{idx}/{len(image_files)}] {conf_color} {image_path.name}")
            print(f"  → {result['prediction']} ({result['confidence']*100:.1f}%)")
            print(f"     Benign: {result['benign_score']*100:.1f}% | Malignant: {result['malignant_score']*100:.1f}%")
    
    return results

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 100)
    print("THYROID NODULE CLASSIFICATION - INFERENCE")
    print("=" * 100)
    print()
    
    # Load model
    print("[1] Loading Model")
    print("-" * 100)
    model, device = load_model()
    print()
    
    # Get transforms
    image_transforms = get_transforms()
    
    # Get input path
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python inference.py image.jpg")
        print("  python inference.py image_folder/")
        print()
        print("Quick Test - Using default benign image:")
        
        # Try to find a benign image
        benign_dir = Path("Datasets for classification/benign")
        if benign_dir.exists():
            images = list(benign_dir.glob("*.jpg")) + list(benign_dir.glob("*.png"))
            if images:
                input_path = images[0]
                print(f"Testing: {input_path}")
            else:
                print("No images found in benign folder")
                sys.exit(1)
        else:
            print(f"Benign dataset not found at: {benign_dir}")
            sys.exit(1)
    else:
        input_path = Path(sys.argv[1])
    
    print()
    print("[2] Running Inference")
    print("-" * 100)
    print()
    
    # Run inference
    if input_path.is_dir():
        results = predict_directory(input_path, model, device, image_transforms)
    else:
        result = predict_image(input_path, model, device, image_transforms)
        results = [result]
    
    # Summary
    print()
    print("[3] Summary")
    print("-" * 100)
    
    benign_count = sum(1 for r in results if r['prediction'] == 'Benign' and not r['error'])
    malignant_count = sum(1 for r in results if r['prediction'] == 'Malignant' and not r['error'])
    error_count = sum(1 for r in results if r['error'])
    total = len(results)
    
    print(f"Total Images: {total}")
    print(f"  ✓ Benign: {benign_count}")
    print(f"  ✓ Malignant: {malignant_count}")
    print(f"  ✗ Errors: {error_count}")
    
    if results:
        avg_confidence = np.mean([r['confidence'] for r in results if not r['error']])
        print(f"  Average Confidence: {avg_confidence*100:.1f}%")
    
    print()
    print("=" * 100)
    print("Interpretation Guide:")
    print("  Benign: Image likely shows benign thyroid nodule")
    print("  Malignant: Image likely shows malignant thyroid nodule")
    print("  Confidence: How certain the model is (higher = more certain)")
    print()
    print("⚠️  DISCLAIMER: This is an AI model for research purposes only.")
    print("    Always consult medical professionals for clinical diagnosis.")
    print("=" * 100)

if __name__ == "__main__":
    main()

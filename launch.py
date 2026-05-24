#!/usr/bin/env python3
"""Launch the Thyroid Nodule Detection & Classification Flask API."""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the app
from backend.app.app import app, load_pipeline, create_app

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🦢 THYROID NODULE DETECTION & CLASSIFICATION SYSTEM")
    print("="*80)
    print("📍 Backend: http://localhost:5000")
    print("🌐 Frontend: http://localhost:5000")
    print("="*80 + "\n")
    
    # Initialize app (sets up database and loads pipeline)
    app = create_app()
    
    # Ensure pipeline loaded
    if load_pipeline():
        print("✓ Pipeline loaded successfully\n")
    else:
        print("⚠ Warning: Pipeline failed to load. Check model paths.\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False
    )


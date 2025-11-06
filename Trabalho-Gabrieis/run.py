#!/usr/bin/env python3
"""
Run script for Flask application in Replit environment
Configures the app to run on 0.0.0.0:5000
"""
import os
import sys

# Add the sgbu_equipe3_emprestimos directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sgbu_equipe3_emprestimos'))

from app.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

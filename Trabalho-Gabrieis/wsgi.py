#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sgbu_equipe3_emprestimos'))

from app.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

#!/usr/bin/env python3
"""
AI Video Generator Setup Script
Automates the installation and startup process for the AI video generator project.
"""

import os
import sys
import subprocess
import platform
import time

def print_banner():
    """Print project banner"""
    print("=" * 60)
    print("🎬 AI Video Generator - Setup Script")
    print("=" * 60)
    print("This script will help you set up and run the AI video generator.")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_backend_dependencies():
    """Install backend Python dependencies"""
    print("\n📦 Installing backend dependencies...")
    
    backend_dir = os.path.join(os.getcwd(), "backend")
    requirements_file = os.path.join(backend_dir, "requirements.txt")
    
    if not os.path.exists(requirements_file):
        print("❌ Error: requirements.txt not found in backend directory")
        sys.exit(1)
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", requirements_file
        ], check=True, cwd=backend_dir)
        print("✅ Backend dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing backend dependencies: {e}")
        sys.exit(1)

def create_output_directories():
    """Create necessary output directories"""
    print("\n📁 Creating output directories...")
    
    backend_output = os.path.join(os.getcwd(), "backend", "outputs")
    os.makedirs(backend_output, exist_ok=True)
    print(f"✅ Created: {backend_output}")

def start_backend():
    """Start the backend server"""
    print("\n🚀 Starting backend server...")
    print("Backend will be available at: http://localhost:8000")
    print("Press Ctrl+C to stop the backend server")
    print()
    
    backend_dir = os.path.join(os.getcwd(), "backend")
    main_file = os.path.join(backend_dir, "main.py")
    
    try:
        subprocess.run([sys.executable, main_file], cwd=backend_dir)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

def start_frontend():
    """Start the frontend server"""
    print("\n🌐 Starting frontend server...")
    print("Frontend will be available at: http://localhost:3000")
    print("Press Ctrl+C to stop the frontend server")
    print()
    
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    
    try:
        subprocess.run([sys.executable, "-m", "http.server", "3000"], cwd=frontend_dir)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_backend_dependencies()
    
    # Create directories
    create_output_directories()
    
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    print("\nTo run the application:")
    print("1. Start backend: python setup.py --backend")
    print("2. Start frontend: python setup.py --frontend")
    print("3. Or run both: python setup.py --run")
    print()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--backend":
            start_backend()
        elif sys.argv[1] == "--frontend":
            start_frontend()
        elif sys.argv[1] == "--run":
            print("Starting both backend and frontend...")
            print("Backend: http://localhost:8000")
            print("Frontend: http://localhost:3000")
            print("Press Ctrl+C to stop both servers")
            
            # Start backend in background
            backend_dir = os.path.join(os.getcwd(), "backend")
            backend_process = subprocess.Popen([sys.executable, "main.py"], cwd=backend_dir)
            
            # Wait a moment for backend to start
            time.sleep(3)
            
            # Start frontend
            frontend_dir = os.path.join(os.getcwd(), "frontend")
            try:
                subprocess.run([sys.executable, "-m", "http.server", "3000"], cwd=frontend_dir)
            except KeyboardInterrupt:
                print("\n🛑 Stopping servers...")
                backend_process.terminate()
                print("✅ Servers stopped")
    else:
        main()

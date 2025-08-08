"""
AETHER - Main Runner Script
© 2024 AlgoRythm Tech - Built by Sri Aasrith Souri Kompella
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser
from pathlib import Path
import logging
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ASCII Art Banner
BANNER = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     █████╗ ███████╗████████╗██╗  ██╗███████╗██████╗                        ║
║    ██╔══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗                       ║
║    ███████║█████╗     ██║   ███████║█████╗  ██████╔╝                       ║
║    ██╔══██║██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗                       ║
║    ██║  ██║███████╗   ██║   ██║  ██║███████╗██║  ██║                       ║
║    ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                       ║
║                                                                              ║
║    Advanced Engine for Thought, Heuristic Emotion and Reasoning             ║
║                                                                              ║
║    🏢 AlgoRythm Tech - The World's First Fully Teen-Built Startup           ║
║    👤 CEO & Founder: Sri Aasrith Souri Kompella                             ║
║    🚀 Revolutionizing AI - One Mind at a Time                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

class AETHERLauncher:
    """Launcher for AETHER AI System"""
    
    def __init__(self):
        self.api_process = None
        self.web_process = None
        self.api_port = 8000
        self.web_port = 8501
        self.project_root = Path(__file__).parent
        
    def print_banner(self):
        """Print the AETHER banner"""
        print("\033[95m" + BANNER + "\033[0m")
        print("=" * 80)
        print("🚀 Starting AETHER AI System...")
        print("=" * 80)
        print()
    
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        logger.info("Checking dependencies...")
        
        required_packages = [
            "torch", "transformers", "fastapi", "streamlit", 
            "uvicorn", "pydantic", "langchain"
        ]
        
        missing = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing:
            logger.warning(f"Missing packages: {', '.join(missing)}")
            logger.info("Installing missing packages...")
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing, check=True)
        else:
            logger.info("✅ All dependencies are installed")
    
    def start_api_server(self):
        """Start the FastAPI backend server"""
        logger.info(f"Starting API server on port {self.api_port}...")
        
        api_path = self.project_root / "api" / "main.py"
        cmd = [
            sys.executable, "-m", "uvicorn",
            "api.main:app",
            "--host", "0.0.0.0",
            "--port", str(self.api_port),
            "--reload"
        ]
        
        self.api_process = subprocess.Popen(
            cmd,
            cwd=self.project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        logger.info(f"✅ API server started at http://localhost:{self.api_port}")
        logger.info(f"📚 API Documentation: http://localhost:{self.api_port}/docs")
    
    def start_web_interface(self):
        """Start the Streamlit web interface"""
        logger.info(f"Starting web interface on port {self.web_port}...")
        
        web_path = self.project_root / "web" / "app.py"
        env = os.environ.copy()
        env["API_URL"] = f"http://localhost:{self.api_port}"
        
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            str(web_path),
            "--server.port", str(self.web_port),
            "--server.address", "0.0.0.0",
            "--theme.primaryColor", "#667eea",
            "--theme.backgroundColor", "#f5f7fa",
            "--theme.secondaryBackgroundColor", "#ffffff",
            "--theme.textColor", "#262730"
        ]
        
        self.web_process = subprocess.Popen(
            cmd,
            cwd=self.project_root,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        logger.info(f"✅ Web interface started at http://localhost:{self.web_port}")
    
    def wait_for_service(self, url, timeout=30):
        """Wait for a service to become available"""
        import requests
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return True
            except:
                pass
            time.sleep(1)
        return False
    
    def open_browser(self):
        """Open the web interface in the default browser"""
        time.sleep(3)  # Wait for services to start
        
        url = f"http://localhost:{self.web_port}"
        logger.info(f"Opening AETHER in your browser: {url}")
        
        try:
            webbrowser.open(url)
        except:
            logger.warning("Could not open browser automatically")
            logger.info(f"Please open your browser and navigate to: {url}")
    
    def run(self, mode="full", no_browser=False):
        """Run AETHER in specified mode"""
        self.print_banner()
        
        try:
            # Check dependencies
            self.check_dependencies()
            
            if mode in ["full", "api"]:
                # Start API server
                self.start_api_server()
                
                # Wait for API to be ready
                if self.wait_for_service(f"http://localhost:{self.api_port}/health"):
                    logger.info("✅ API server is ready")
                else:
                    logger.error("API server failed to start")
                    return
            
            if mode in ["full", "web"]:
                # Start web interface
                self.start_web_interface()
                
                # Open browser
                if not no_browser:
                    threading.Thread(target=self.open_browser).start()
            
            # Print success message
            print("\n" + "=" * 80)
            print("🎉 AETHER is now running!")
            print("=" * 80)
            print()
            print("📍 Access Points:")
            print(f"   Web Interface: http://localhost:{self.web_port}")
            print(f"   API Endpoint:  http://localhost:{self.api_port}")
            print(f"   API Docs:      http://localhost:{self.api_port}/docs")
            print()
            print("💡 Tips:")
            print("   - Customize AETHER using the sidebar in the web interface")
            print("   - Check API documentation for programmatic access")
            print("   - Press Ctrl+C to stop AETHER")
            print()
            print("🏢 Built with ❤️ by AlgoRythm Tech")
            print("👤 CEO: Sri Aasrith Souri Kompella")
            print()
            
            # Keep running
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Shutting down AETHER...")
            self.shutdown()
        except Exception as e:
            logger.error(f"Error: {e}")
            self.shutdown()
    
    def shutdown(self):
        """Shutdown all services"""
        if self.api_process:
            logger.info("Stopping API server...")
            self.api_process.terminate()
            self.api_process.wait()
        
        if self.web_process:
            logger.info("Stopping web interface...")
            self.web_process.terminate()
            self.web_process.wait()
        
        logger.info("✅ AETHER has been shut down successfully")
        print("\nThank you for using AETHER! 👋")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AETHER - Advanced Engine for Thought, Heuristic Emotion and Reasoning"
    )
    
    parser.add_argument(
        "--mode",
        choices=["full", "api", "web"],
        default="full",
        help="Run mode: full (both API and web), api (API only), or web (web only)"
    )
    
    parser.add_argument(
        "--api-port",
        type=int,
        default=8000,
        help="API server port (default: 8000)"
    )
    
    parser.add_argument(
        "--web-port",
        type=int,
        default=8501,
        help="Web interface port (default: 8501)"
    )
    
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Don't open browser automatically"
    )
    
    args = parser.parse_args()
    
    # Create and run launcher
    launcher = AETHERLauncher()
    launcher.api_port = args.api_port
    launcher.web_port = args.web_port
    launcher.run(mode=args.mode, no_browser=args.no_browser)


if __name__ == "__main__":
    main()

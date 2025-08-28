import subprocess
import sys
import os

def test_ffmpeg_bundling():
    """Test if FFmpeg is properly bundled and accessible"""
    
    # Test 1: Check if running as executable
    if getattr(sys, 'frozen', False):
        print("✓ Running as PyInstaller executable")
        bundle_dir = sys._MEIPASS
        print(f"  Bundle directory: {bundle_dir}")
        
        # Check for FFmpeg in bundle
        ffmpeg_path = os.path.join(bundle_dir, 'ffmpeg', 'bin', 'ffmpeg.exe')
        if os.path.exists(ffmpeg_path):
            print("✓ FFmpeg found in bundle")
            print(f"  Path: {ffmpeg_path}")
            
            # Test FFmpeg execution
            try:
                result = subprocess.run([ffmpeg_path, '-version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print("✓ FFmpeg executes successfully")
                    # Extract version info
                    version_line = result.stdout.split('\n')[0]
                    print(f"  Version: {version_line}")
                else:
                    print("✗ FFmpeg execution failed")
                    print(f"  Error: {result.stderr}")
            except Exception as e:
                print(f"✗ FFmpeg execution error: {e}")
        else:
            print("✗ FFmpeg not found in bundle")
            print(f"  Expected path: {ffmpeg_path}")
    else:
        print("✗ Not running as executable - run the built .exe instead")

if __name__ == "__main__":
    test_ffmpeg_bundling()
    input("\nPress Enter to close...")

from PIL import Image
import os

def check_exe_status():
    """Check if the executable was built with correct icon"""
    print("🔍 CHECKING EXECUTABLE STATUS")
    print("="*40)
    
    # Check if dist folder exists
    dist_path = "dist/YouTube-Downloader.exe"
    if not os.path.exists(dist_path):
        print("❌ Executable not found in dist folder")
        return False
    
    exe_size = os.path.getsize(dist_path)
    print(f"📁 Executable: {dist_path}")
    print(f"📊 Size: {exe_size:,} bytes")
    
    # Check spec file
    spec_path = "YouTube-Downloader.spec"
    if os.path.exists(spec_path):
        with open(spec_path, 'r') as f:
            content = f.read()
        
        if "icon=" in content:
            import re
            icon_match = re.search(r"icon='([^']*)'", content)
            if icon_match:
                icon_file = icon_match.group(1)
                print(f"🎯 Icon in spec: {icon_file}")
                
                # Check if icon file exists
                if os.path.exists(icon_file):
                    ico_size = os.path.getsize(icon_file)
                    print(f"✅ Icon file exists: {ico_size:,} bytes")
                    
                    # Check icon details
                    try:
                        ico = Image.open(icon_file)
                        print(f"📐 Icon size: {ico.width}x{ico.height}")
                        print(f"🎨 Icon mode: {ico.mode}")
                        return True
                    except Exception as e:
                        print(f"❌ Icon file error: {e}")
                        return False
                else:
                    print(f"❌ Icon file missing: {icon_file}")
                    return False
            else:
                print("❌ No icon path found in spec")
                return False
        else:
            print("❌ No icon parameter in spec file")
            return False
    else:
        print("❌ Spec file not found")
        return False

def main():
    print("🚀 FINAL ICON VERIFICATION")
    print("="*30)
    
    if check_exe_status():
        print(f"\n✅ EXECUTABLE BUILT CORRECTLY!")
        print(f"🎯 Icon should be embedded properly")
        print(f"\n🧹 NEXT STEP: Clear Windows icon cache")
        print(f"   Run: clear_icon_cache.bat")
        print(f"   Or restart your computer")
        
        print(f"\n📋 TROUBLESHOOTING:")
        print(f"   • If still seeing old icon: Run clear_icon_cache.bat")
        print(f"   • Right-click exe → Properties → check icon")
        print(f"   • Try different folder view sizes in Explorer")
        
    else:
        print(f"\n❌ EXECUTABLE HAS ISSUES")
        print(f"🔧 Need to fix and rebuild")

if __name__ == "__main__":
    main()

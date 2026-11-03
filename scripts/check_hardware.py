"""Show detected hardware and conservative TTS recommendations."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.hardware_profile import main

if __name__ == '__main__':
    main()

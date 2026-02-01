#!/usr/bin/env python3
"""Test Q10 CLI commands with authenticated session"""
import asyncio
import subprocess
import sys
import pickle
import os

def get_device_id():
    """Get device_id from cache"""
    cache_path = os.path.expanduser("~/.cache/roborock-cache-data.pkl")
    try:
        with open(cache_path, 'rb') as f:
            data = pickle.load(f)
            if hasattr(data, 'home_data') and data.home_data:
                devices = data.home_data.devices
                if devices:
                    return devices[0].duid
    except Exception as e:
        print(f"Error reading cache: {e}")
    return None

async def test_cli_command(command, device_id):
    """Test a CLI command"""
    print(f"Testing: {command}")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "roborock.cli", command, "--device_id", device_id],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"   ✅ SUCCESS")
            return True
        else:
            error_msg = result.stderr if result.stderr else result.stdout
            print(f"   ❌ FAILED: {error_msg[:80]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"   ❌ TIMEOUT")
        return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

async def main():
    """Test all 5 Q10 CLI commands"""
    device_id = get_device_id()
    if not device_id:
        print("❌ Could not find device_id in cache")
        return
    
    print("=" * 60)
    print("Testing Q10 Vacuum CLI Commands")
    print("=" * 60)
    print(f"Device ID: {device_id}\n")
    
    commands = [
        "q10-vacuum-start",
        "q10-vacuum-pause",
        "q10-vacuum-resume",
        "q10-vacuum-stop",
        "q10-vacuum-dock",
    ]
    
    results = []
    for i, cmd in enumerate(commands, 1):
        print(f"{i}️⃣  {cmd}")
        success = await test_cli_command(cmd, device_id)
        results.append((cmd, success))
        print()
        await asyncio.sleep(1.5)
    
    print("=" * 60)
    print("Summary:")
    print("=" * 60)
    for cmd, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {cmd}")
    
    total = len(results)
    passed = sum(1 for _, s in results if s)
    print(f"\nTotal: {passed}/{total} commands passed")

if __name__ == "__main__":
    asyncio.run(main())

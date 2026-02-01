#!/usr/bin/env python3
"""Quick test script for Q10 CLI commands using the device manager."""

import asyncio
import pathlib
from roborock.devices.device_manager import create_device_manager
from roborock.devices.file_cache import FileCache, load_value, store_value

USER_PARAMS_PATH = pathlib.Path.home() / ".cache" / "roborock-user-params.pkl"
CACHE_PATH = pathlib.Path.home() / ".cache" / "roborock-cache-data.pkl"


async def main():
    """Test Q10 CLI commands."""
    print("🔄 Loading cached credentials...")
    user_params = await load_value(USER_PARAMS_PATH)
    if user_params is None:
        print("❌ No cached credentials found!")
        print("   Run: python examples/Q10/run_q10_simple.py first")
        return
    
    cache = FileCache(CACHE_PATH)
    
    print("🔄 Creating device manager...")
    device_manager = await create_device_manager(user_params, cache=cache)
    
    print("🔄 Getting devices...")
    devices = await device_manager.get_devices()
    
    print(f"\n📱 Found {len(devices)} device(s)")
    for idx, device in enumerate(devices, 1):
        print(f"  {idx}. {device.name} ({device.product.model})")
    
    if len(devices) == 0:
        print("❌ No devices found!")
        return
    
    device = devices[0]
    
    if device.b01_q10_properties is None:
        print(f"\n❌ Device {device.name} is not a Q10 device!")
        return
    
    vacuum = device.b01_q10_properties.vacuum
    
    print(f"\n✅ Device: {device.name}")
    print(f"   Model: {device.product.model}")
    print(f"   Connected: {device.is_connected}")
    
    # Test commands
    print("\n" + "=" * 50)
    print("🧪 TESTING CLI COMMANDS")
    print("=" * 50)
    
    commands = [
        ("Start cleaning", vacuum.start_clean),
        ("Pause cleaning", vacuum.pause_clean),
        ("Resume cleaning", vacuum.resume_clean),
        ("Stop cleaning", vacuum.stop_clean),
        ("Return to dock", vacuum.return_to_dock),
    ]
    
    for name, cmd in commands:
        try:
            print(f"\n▶️  Testing: {name}")
            await cmd()
            print(f"   ✅ Command sent successfully!")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    await cache.flush()
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())

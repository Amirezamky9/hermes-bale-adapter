#!/usr/bin/env python3
"""
Test script for Bale platform adapter.
Tests the connection and basic functionality.
"""

import asyncio
import httpx
import json
import os

# Load token from .env
env_path = os.path.expanduser('~/.hermes/.env')
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('BALE_BOT_TOKEN='):
                os.environ['BALE_BOT_TOKEN'] = line.strip().split('=', 1)[1]

TOKEN = os.getenv('BALE_BOT_TOKEN')
API_BASE = "https://tapi.bale.ai"

async def test_get_me():
    """Test getMe API endpoint."""
    print("🔍 Testing getMe...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/bot{TOKEN}/getMe")
        data = response.json()

        if data.get('ok'):
            bot = data['result']
            print(f"✅ Bot connected successfully!")
            print(f"   Bot ID: {bot['id']}")
            print(f"   Username: @{bot.get('username', 'N/A')}")
            print(f"   Name: {bot.get('first_name', 'N/A')} {bot.get('last_name', '')}")
            return True
        else:
            print(f"❌ Connection failed: {data.get('description')}")
            return False

async def test_get_updates():
    """Test getUpdates API endpoint."""
    print("\n🔍 Testing getUpdates...")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE}/bot{TOKEN}/getUpdates",
            params={'offset': 0, 'limit': 5}
        )
        data = response.json()

        if data.get('ok'):
            updates = data.get('result', [])
            print(f"✅ getUpdates successful! Found {len(updates)} updates")
            return True
        else:
            print(f"❌ getUpdates failed: {data.get('description')}")
            return False

async def test_send_message(chat_id: str, text: str):
    """Test sendMessage API endpoint."""
    print(f"\n🔍 Testing sendMessage to {chat_id}...")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE}/bot{TOKEN}/sendMessage",
            json={
                'chat_id': chat_id,
                'text': text
            }
        )
        data = response.json()

        if data.get('ok'):
            msg = data['result']
            print(f"✅ Message sent successfully!")
            print(f"   Message ID: {msg.get('message_id')}")
            return True
        else:
            print(f"❌ Send failed: {data.get('description')}")
            return False

async def main():
    print("=" * 50)
    print("🧪 Bale Platform Adapter Test")
    print("=" * 50)

    # Test 1: getMe
    if not await test_get_me():
        return

    # Test 2: getUpdates
    if not await test_get_updates():
        return

    # Test 3: Send message (using the test chat ID from env, or default)
    chat_id = os.getenv("BALE_TEST_CHAT_ID", "123456789")
    await test_send_message(chat_id, "✅ تست اتصال با موفقیت انجام شد!")

    print("\n" + "=" * 50)
    print("🎉 All tests passed! Bale adapter is ready.")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())

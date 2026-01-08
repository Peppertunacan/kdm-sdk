import asyncio
from kdm_sdk import KDMClient

async def main():
    client = KDMClient() # 기본값 http://203.237.1.4/mcp/sse 사용
    print(f"Connecting to {client.server_url}...")
    try:
        # 1. 연결 시도
        await asyncio.wait_for(client.connect(), timeout=5.0)
        print("✅ Connected successfully!")
        
        # 2. 헬스 체크
        is_healthy = await client.health_check()
        print(f"✅ Server health: {'Healthy' if is_healthy else 'Unhealthy'}")
        
        # 3. 간단한 데이터 조회 (소양강댐 저수율)
        print("Querying data for 소양강댐...")
        result = await client.get_water_data(
            site_name="소양강댐", 
            facility_type="dam", 
            measurement_items=["저수율"], 
            days=1
        )
        if result.get("success"):
            print("✅ Data retrieval successful!")
            print(f"Result: {result.get('data')[:1]}")
        else:
            print(f"❌ Data retrieval failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Connection/Query failed: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

# test_client.py
import asyncio
from fastmcp import Client
import json


async def main():
    async with Client("http://127.0.0.1:8000/mcp") as client:
        # Test GET all
        all_objects = await client.call_tool("get_all_objects", {})   
        print("All objects:", all_objects)

        # Test POST
        new_obj = {"name": "MCP Widget", "data": {"type": "demo"}}
        created = await client.call_tool("add_object", {"data": new_obj})
        print("Created object:", created)

        # 1. Access the TextContent object (it's the first and only item in the list)
        text_content_obj = created[0]

        # 2. Get the 'text' attribute, which contains the JSON string
        json_string = text_content_obj.text

        # 3. Parse the JSON string into a Python dictionary
        parsed_data = json.loads(json_string)

        # 4. # Extract ID Fetch the 'id' from the dictionary
        object_id = parsed_data.get("id")

        print("Fetched created_id:", object_id)
        # Test GET single
        single = await client.call_tool("get_object_by_id", {"object_id": object_id})
        print("Fetched single:", single)

        # Test PUT
        updated = await client.call_tool("update_object", {
            "object_id": object_id,
            "data": {"name": "Updated Widget", "data": {"type": "full update"}}
        })
        print("Updated:", updated)

        # Test PATCH
        patched = await client.call_tool("patch_object", {
            "object_id": object_id,
            "data": {"name": "Partially Updated Widget"}
        })
        print("Patched:", patched)

        # Test DELETE
        deleted = await client.call_tool("delete_object", {"object_id": object_id})
        print("Deleted:", deleted)

if __name__ == "__main__":
    asyncio.run(main())

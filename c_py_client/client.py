import asyncio
from image_service_client import ImageServiceClient


async def list_images():
    async with ImageServiceClient() as client:
        response = client.list_images()
        print(response)


if __name__ == "__main__":
    asyncio.run(list_images())
import httpx
from fastapi import Request, Response


async def proxy_request(request: Request, target_url: str) -> Response:
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method,
            target_url,
            headers={
                key.decode(): value.decode()
                for key, value in request.headers.raw
                if key.decode().lower() != "host"
            },
            content=await request.body(),
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )

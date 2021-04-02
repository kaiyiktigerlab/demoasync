import time
import httpx
import asyncio

from django.http import JsonResponse


def api(request):
    time.sleep(1)
    payload = {"message": "Hello World!"}
    if "task_id" in request.GET:
        payload["task_id"] = request.GET["task_id"]
    return JsonResponse(payload)


def get_api_urls(num=10):
    base_url = "http://127.0.0.1:8000/api/"
    return [f"{base_url}?task_id={task_id}" for task_id in range(num)]


async def api_aggregated(request):
    s = time.perf_counter()
    responses = []
    urls = get_api_urls(num=10)
    async with httpx.AsyncClient() as client:
        responses = await asyncio.gather(*[client.get(url) for url in urls])
        responses = [r.json() for r in responses]
    elapsed = time.perf_counter() - s
    result = {
        "message": "Hello Async World!",
        "responses": responses,
        "debug_message": f"fetch executed in {elapsed:0.2f} seconds.",
    }
    return JsonResponse(result)


def api_aggregated_sync(request):
    s = time.perf_counter()
    responses = []
    urls = get_api_urls(num=10)
    for url in urls:
        r = httpx.get(url)
        responses.append(r.json())
    elapsed = time.perf_counter() - s
    result = {
        "message": "Hello Sync World!",
        "aggregated_responses": responses,
        "debug_message": f"fetch executed in {elapsed:0.2f} seconds.",
    }
    return JsonResponse(result)
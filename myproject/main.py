import os

import pytz  # timezone object create
import django
from fastapi import FastAPI

from myproject import settings
from schemas import Schema
from asgiref.sync import sync_to_async

# django configuration setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

app = FastAPI(
    title="fast_api",
    description="Test project",
    version="1.0.0",
)

# import here because django configuration needed at this point
from fast_api.models import EndpointStates


@app.post("/test")
async def process_data(schema: Schema):
    # timezone specification
    timezone = pytz.timezone(settings.TIME_ZONE)
    input_start_naive = schema.input_start
    input_start_aware = timezone.localize(input_start_naive)  # put info about timezone
    input_start_timestamp = input_start_aware.timestamp()

    # Filter case: endpoint_state where state_start >= input_start and endpoint_id = 139
    records = await sync_to_async(list)(
        EndpointStates.objects.filter(
            state_start__gte=input_start_timestamp, endpoint_id=139
        ).order_by("-state_start")
    )

    # choose rows where id % 3 == 0
    filtered_records = [record for record in records if record.id % 3 == 0]

    # choose third filtered row
    third_record = filtered_records[2]

    client_info = await sync_to_async(lambda: third_record.client.client_info.info)()

    return {
        "filtered_count": len(filtered_records),
        "client_info": client_info,
        "state_id": third_record.state_id,
    }

from typing import List, Optional

import fastapi

from models.location import Location
from models.reports import Report, ReportSubmittal
from models.validation_error import ValidationError
from services import openweather_service, report_service

router = fastapi.APIRouter()


@router.get('/api/weather/{city}')
async def weather(
    loc: Location = fastapi.Depends(), units: Optional[str] = 'metric'
):
    try:
        return await openweather_service.get_report_async(
            loc.city, loc.state, loc.country, units
        )
    except ValidationError as ve:
        return fastapi.Response(
            content=ve.error_msg, status_code=ve.status_code
        )


@router.get('/api/reports', name='all_reports', response_model=List[Report])
async def reports_get() -> List[Report]:
    # await report_service.add_report('A', Location(city='Santiago'))
    # await report_service.add_report('B', Location(city='Viña'))
    return await report_service.get_reports()


@router.post(
    '/api/reports', name='all_reports', status_code=201, response_model=Report
)
async def reports_post(report_submittal: ReportSubmittal) -> Report:
    d = report_submittal.description
    loc = report_submittal.location
    return await report_service.add_report(d, loc)

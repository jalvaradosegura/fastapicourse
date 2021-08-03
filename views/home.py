import fastapi
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from services import report_service

templates = Jinja2Templates('templates')
router = fastapi.APIRouter()


@router.get('/', include_in_schema=False)
async def index(request: Request):
    events = await report_service.get_reports()
    return templates.TemplateResponse(
        '/home/index.html', {'request': request, 'events': events}
    )


@router.get('/favicon.icon', include_in_schema=False)
def favicon():
    return fastapi.responses.RedirectResponse(url='/static/img/favicon.ico')
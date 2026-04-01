from fastapi import APIRouter
from app.api.v1.endpoints import analyze, compare, translate, report

api_router = APIRouter()

# Register routers
api_router.include_router(analyze.router, prefix='/analyze', tags=['analyze'])
api_router.include_router(compare.router, prefix='/compare', tags=['compare'])
api_router.include_router(translate.router, prefix='/translate', tags=['translate'])
api_router.include_router(report.router, prefix='/report', tags=['report'])
# app/api.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from . import services
from .schemas import AnalysisResponse

router = APIRouter()

@router.post("/analyze-architecture/", response_model=AnalysisResponse)
async def analyze_architecture(file: UploadFile = File(...)):
    """
    Recebe uma imagem de um diagrama de arquitetura, analisa usando a metodologia STRIDE
    e retorna um JSON com as ameaças e mitigações.
    """
    # Verifica se o arquivo é uma imagem
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="O arquivo enviado não é uma imagem.")

    try:
        image_bytes = await file.read()
        analysis_result = services.analyze_architecture_image(image_bytes)
        return analysis_result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro inesperado: {str(e)}")
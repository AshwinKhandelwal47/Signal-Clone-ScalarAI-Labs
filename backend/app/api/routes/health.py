from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, bool]:
    """Basic service health check endpoint."""
    return {"ok": True}


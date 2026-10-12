<<<<<<< HEAD
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}
=======
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, bool]:
    """Basic service health check endpoint."""
    return {"ok": True}

>>>>>>> 653fe1e (commented code)

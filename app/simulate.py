from dataclasses import dataclass, field

from fastapi import APIRouter

from metrics import MEMORY_LEAK_BYTES

router = APIRouter(prefix="/simulate", tags=["simulation"])


@dataclass
class SimulationState:
    slow_enabled: bool = False
    errors_enabled: bool = False
    memory_leak_enabled: bool = False
    _leak_store: list = field(default_factory=list)


simulation_state = SimulationState()


@router.post("/slow")
async def set_slow(enabled: bool = True):
    simulation_state.slow_enabled = enabled
    return {"slow_enabled": simulation_state.slow_enabled}


@router.post("/errors")
async def set_errors(enabled: bool = True):
    simulation_state.errors_enabled = enabled
    return {"errors_enabled": simulation_state.errors_enabled}


@router.post("/memory-leak")
async def set_memory_leak(enabled: bool = True):
    simulation_state.memory_leak_enabled = enabled
    if not enabled:
        simulation_state._leak_store.clear()
        MEMORY_LEAK_BYTES.set(0)
    return {"memory_leak_enabled": simulation_state.memory_leak_enabled}


@router.post("/reset")
async def reset_all():
    simulation_state.slow_enabled = False
    simulation_state.errors_enabled = False
    simulation_state.memory_leak_enabled = False
    simulation_state._leak_store.clear()
    MEMORY_LEAK_BYTES.set(0)
    return {"status": "all simulations reset"}


@router.get("/status")
async def get_status():
    return {
        "slow_enabled": simulation_state.slow_enabled,
        "errors_enabled": simulation_state.errors_enabled,
        "memory_leak_enabled": simulation_state.memory_leak_enabled,
        "leak_size_mb": round(len(simulation_state._leak_store) * 102400 / 1024 / 1024, 2),
    }

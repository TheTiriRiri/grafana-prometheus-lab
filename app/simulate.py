from dataclasses import dataclass, field

from fastapi import APIRouter

router = APIRouter(prefix="/simulate", tags=["simulation"])


@dataclass
class SimulationState:
    slow_enabled: bool = False
    errors_enabled: bool = False
    memory_leak_enabled: bool = False
    _leak_store: list = field(default_factory=list)


simulation_state = SimulationState()


@router.post("/slow")
async def toggle_slow():
    simulation_state.slow_enabled = not simulation_state.slow_enabled
    return {"slow_enabled": simulation_state.slow_enabled}


@router.post("/errors")
async def toggle_errors():
    simulation_state.errors_enabled = not simulation_state.errors_enabled
    return {"errors_enabled": simulation_state.errors_enabled}


@router.post("/memory-leak")
async def toggle_memory_leak():
    simulation_state.memory_leak_enabled = not simulation_state.memory_leak_enabled
    if not simulation_state.memory_leak_enabled:
        simulation_state._leak_store.clear()
    return {"memory_leak_enabled": simulation_state.memory_leak_enabled}


@router.post("/reset")
async def reset_all():
    simulation_state.slow_enabled = False
    simulation_state.errors_enabled = False
    simulation_state.memory_leak_enabled = False
    simulation_state._leak_store.clear()
    return {"status": "all simulations reset"}


@router.get("/status")
async def get_status():
    return {
        "slow_enabled": simulation_state.slow_enabled,
        "errors_enabled": simulation_state.errors_enabled,
        "memory_leak_enabled": simulation_state.memory_leak_enabled,
        "leak_size_mb": round(len(simulation_state._leak_store) * 102400 / 1024 / 1024, 2),
    }

import json
from pathlib import Path
from app.core.config import settings
from app.shared.exceptions import ServioException

class RegistryBuilderService:
    def __init__(self):
        self.data_path = Path("data/servio_data.jsonl")

    async def add_service(self, service_data: dict):
        try:
            with open(self.data_path, "a") as f:
                f.write(json.dumps(service_data) + "\n")
            return {"status": "success", "service": service_data}
        except Exception as e:
            raise ServioException(f"Failed to add service: {str(e)}")

    async def rebuild_registry(self):
        raise NotImplementedError("Registry rebuild not yet implemented")
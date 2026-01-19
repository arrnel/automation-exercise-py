from src.config.config import CFG
from src.model.enum.remote_type import RemoteType
from src.service.remote.moon_artifact_service import MoonArtifactApiService
from src.service.remote.remote_artifact_service import RemoteArtifactsService
from src.service.remote.selenoid_artifact_service import SelenoidArtifactApiService


def instance() -> RemoteArtifactsService:
    match CFG.remote_type:
        case RemoteType.SELENOID:
            return SelenoidArtifactApiService()
        case RemoteType.MOON:
            return MoonArtifactApiService()
        case RemoteType.NONE:
            raise RuntimeError("Remote resources are disabled")

import importlib.util
import inspect
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI


def service_name_validation(name: str) -> None | ValueError:
    if any(c in name for c in " /\\.:?\"<>|*[]=;,!@#$%^&(){}+`~'"):
        raise ValueError(
            f"Service name: {name} should contain only alphabets, numbers, and underscores."
        )


class Singularity(FastAPI):
    def __init__(self, env_path: str = None):
        self.base_path = Path(inspect.stack()[1].filename).parent
        self.services_folder = self.base_path / "services"
        self._load_env_(env_path)
        self._setup_application_()

    def _load_env_(self, path: str | None):
        if path is None:
            path = os.path.join(self.base_path, ".env")

        if not os.path.exists(path):
            raise ValueError(f"Environment file not found in {path}")

        load_dotenv(dotenv_path=path)

    def _setup_application_(
        self,
    ):
        self.app = FastAPI()
        self.router = APIRouter()
        self.register_services()
        self.app.include_router(self.router)

    def __getattr__(self, name):
        # This method is called when an attribute is not found in the usual places.
        # It delegates attribute access to the FastAPI instance.
        return getattr(self.app, name)

    def register_services(self):
        for service_name in os.listdir(self.services_folder):
            # validate service name
            service_name_validation(service_name)

            if os.path.isdir(
                os.path.join(self.services_folder, service_name)
            ) and os.path.exists(
                os.path.join(self.services_folder, service_name, "service.py")
            ):
                spec = importlib.util.spec_from_file_location(
                    "service", f"{self.services_folder}/{service_name}/service.py"
                )
                module = importlib.util.module_from_spec(spec)
                module.__package__ = f"services.{service_name}"
                spec.loader.exec_module(module)

                if hasattr(module, "Service"):
                    service_class = getattr(module, "Service")
                    service_instance = service_class()
                    if hasattr(service_instance, "get"):
                        self.router.add_api_route(
                            f"/{service_name}",
                            getattr(service_instance, "get"),
                            methods=["GET"],
                        )
                    if hasattr(service_instance, "post"):
                        self.router.add_api_route(
                            f"/{service_name}",
                            getattr(service_instance, "post"),
                            methods=["POST"],
                        )
                    if hasattr(service_instance, "put"):
                        self.router.add_api_route(
                            f"/{service_name}",
                            getattr(service_instance, "put"),
                            methods=["PUT"],
                        )
                    if hasattr(service_instance, "delete"):
                        self.router.add_api_route(
                            f"/{service_name}",
                            getattr(service_instance, "delete"),
                            methods=["DELETE"],
                        )
                else:
                    raise ValueError(f"Service class not found in {service_name}")
            else:
                raise ValueError(f"Service file not found in {service_name}")

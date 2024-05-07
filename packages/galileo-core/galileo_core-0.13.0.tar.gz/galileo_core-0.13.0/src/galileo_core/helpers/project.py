from typing import Optional

from pydantic import UUID4
from requests import get, post

from galileo_core.constants.routes import Routes
from galileo_core.helpers.config import GalileoConfig
from galileo_core.logger import logger
from galileo_core.schemas.core.project import CreateProjectRequest, ProjectResponse


def create_project(request: CreateProjectRequest, config: GalileoConfig) -> ProjectResponse:
    existing_project = get_project_from_name(request.name, config=config, raise_if_missing=False)
    if existing_project:
        logger.debug(f"Project {request.name} already exists, using it.")
        project_response = existing_project
    else:
        logger.debug(f"Creating project {request.name}...")
        response_dict = config.api_client.request(post, Routes.projects, json=request.model_dump(mode="json"))
        project_response = ProjectResponse.model_validate(response_dict)
        logger.debug(f"Created project with name {project_response.name}, ID {project_response.id}.")
    return project_response


def get_project(project_id: UUID4, config: GalileoConfig) -> ProjectResponse:
    response_dict = config.api_client.request(get, Routes.project.format(project_id=project_id))
    project = ProjectResponse.model_validate(response_dict)
    logger.debug(f"Got project with name {project.name}, ID {project.id}.")
    return project


def get_project_from_name(
    project_name: str, config: GalileoConfig, raise_if_missing: bool = True
) -> Optional[ProjectResponse]:
    projects = [
        ProjectResponse.model_validate(proj)
        for proj in config.api_client.request(get, Routes.projects, params=dict(project_name=project_name))
    ]
    if raise_if_missing and len(projects) == 0:
        raise ValueError(f"Project {project_name} does not exist.")
    elif len(projects) > 0:
        project_response = projects[0]
        logger.debug(f"Got project with name {project_response.name}, with ID {project_response.id}.")
        return project_response
    else:
        return None

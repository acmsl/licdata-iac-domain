# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/domain/licdata_iac.py

This script defines the LicdataIac class.

Copyright (C) 2024-today acm-sl's Licdata IaC Domain

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from pythoneda.shared.artifact.events import DockerImageAvailable, DockerImageRequested
from pythoneda.shared.iac.events import (
    InfrastructureUpdateRequested,
    InfrastructureUpdated,
)
from pythoneda.shared.iac import StackFactory
from pythoneda.shared import EventEmitter, EventListener, Flow, listen, Ports


class LicdataIac(Flow, EventEmitter, EventListener):
    """
    Licdata Infrastructure as Code.

    Class name: LicdataIac

    Responsibilities:
        - Define the Licdata Infrastructure.

    Collaborators:
        - org.acmsl.licdata.domain.serverless.License
    """

    _singleton = None

    def __init__(self):
        """
        Creates a new LicdataIac instance.
        """
        super().__init__()

    @classmethod
    def instance(cls):
        """
        Retrieves the singleton instance.
        :return: Such instance.
        :rtype: org.acmsl.iac.licdata.domain.LicdataIac
        """
        if cls._singleton is None:
            cls._singleton = cls()

        return cls._singleton

    @classmethod
    @listen(InfrastructureUpdateRequested)
    async def listen_InfrastructureUpdateRequested(
        cls, event: InfrastructureUpdateRequested
    ) -> InfrastructureUpdated:
        """
        Gets notified of a InfrastructureUpdateRequested event.
        :param event: The event.
        :type event: org.acmsl.iac.licdata.domain.InfrastructureUpdateRequested
        """
        cls.instance()._add_event(event)
        cls.logger().info(
            f"Infrastructure update for {event.project_name}/{event.stack_name} at {event.location} requested"
        )
        #        followUp = await cls.instance().update_infrastructure(
        #            event.stack_name, event.project_name, event.location
        #        )

        followUp = InfrastructureUpdated(
            event.stack_name, event.project_name, event.location
        )
        if not followUp.is_error:
            await cls.instance().emit(DockerImageRequested("licdata"))

    async def update_infrastructure(
        self, stackName: str, projectName: str, location: str
    ):
        """
        Updates the infrastructure.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The location.
        :type location: str
        :return: Either an InfrastructureUpdated or InfrastructureNotUpdated event.
        :rtype: org.acmsl.iac.licdata.domain.InfrastructureUpdated
        """
        factory = Ports.instance().resolve_first(StackFactory)
        stack = factory.new(stackName, projectName, location)
        result = await stack.up()
        return result

    @classmethod
    @listen(DockerImageAvailable)
    async def listen_DockerImageAvailable(
        cls, event: DockerImageAvailable
    ) -> InfrastructureUpdated:
        """
        Gets notified of a InfrastructureUpdateRequested event.
        :param event: The event.
        :type event: org.acmsl.iac.licdata.domain.InfrastructureUpdateRequested
        """
        cls.instance().resume(event)

    async def accept(
        self, event: DockerImageAvailable, previousEvent: DockerImageRequested
    ):
        """
        Accepts a DockerImageAvailable event.
        :param event: The event.
        :type event: org.acmsl.iac.licdata.domain.DockerImageAvailable
        :param previousEvent: The previous event.
        :type previousEvent: org.acmsl.iac.licdata.domain.DockerImageRequested
        """
        self.__class__.logger().info(
            f"Docker image available: {event.name}/{event.version} ({event.url})"
        )
        emit(
            await cls.update_docker_resources(
                previousEvent.stack_name,
                previousEvent.project_name,
                previousEvent.location,
                event.name,
                event.version,
                event.url,
            )
        )

    async def update_docker_resources(
        self,
        stackName: str,
        projectName: str,
        location: str,
        imageName: str,
        imageVersion: str,
        imageUrl: str = None,
    ):
        """
        Updates the Docker-dependent infrastructure resources.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The location.
        :type location: str
        :param imageName: The name of the Docker image.
        :type imageName: str
        :param imageVersion: The version of the Docker image.
        :type imageVersion: str
        :param imageUrl: The url of the Docker image.
        :type imageUrl: str
        :return: Either a DockerResourcesUpdated or DockerResourcesUpdateFailed event.
        :rtype: pythoneda.shared.iac.events.DockerResourcesUpdated
        """
        factory = Ports.instance().resolve_first(StackFactory)
        stack = factory.new(stackName, projectName, location)
        result = await stack.declare_docker_resources(imageName, imageVersion, imageUrl)
        return result


# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

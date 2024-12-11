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
    InfrastructureRemovalRequested,
    InfrastructureRemoved,
    InfrastructureUpdateRequested,
    InfrastructureUpdated,
)
from pythoneda.shared.iac import StackFactory
from pythoneda.shared import Event, EventEmitter, EventListener, Flow, listen, Ports
from typing import List


class LicdataIac(Flow, EventListener):
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
    ) -> List[Event]:
        """
        Gets notified of a InfrastructureUpdateRequested event.
        :param event: The event.
        :type event: org.acmsl.iac.licdata.domain.InfrastructureUpdateRequested
        :return: A list of events.
        :rtype: List[org.acmsl.iac.licdata.domain.Event]
        """
        cls.instance().add_event(event)
        cls.logger().info(
            f"Infrastructure update for {event.project_name}/{event.stack_name} at {event.location} requested"
        )
        return await cls.instance().update_infrastructure(
            event.stack_name, event.project_name, event.location
        )

    async def update_infrastructure(
        self, stackName: str, projectName: str, location: str
    ) -> List[Event]:
        """
        Updates the infrastructure.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The location.
        :type location: str
        :return: A list of events.
        :rtype: pythoneda.shared.Event
        """
        factory = Ports.instance().resolve_first(StackFactory)
        stack = factory.new(stackName, projectName, location)
        followUp = await stack.up()
        for event in followUp:
            self.add_event(event)
        result = followUp
        if len(followUp) > 0 and not followUp[-1].is_error:
            request = stack.request_docker_image()
            self.add_event(request)
            result.append(request)
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
        await cls.instance().resume(event)

    async def continue_flow(
        self, event: DockerImageAvailable, previousEvent: DockerImageRequested
    ):
        """
        Continues the flow with a new event.
        :param event: The event.
        :type event: org.acmsl.iac.licdata.domain.DockerImageAvailable
        :param previousEvent: The previous event.
        :type previousEvent: org.acmsl.iac.licdata.domain.DockerImageRequested
        """
        self.__class__.logger().info(
            f"Docker image available: {event.image_name}/{event.image_version} ({event.image_url})"
        )
        infrastructure_updated = self.find_latest_event(InfrastructureUpdated)
        if infrastructure_updated is None:
            self.__class__.logger().error(
                f"Could not find the previous InfrastructureUpdated event"
            )
        else:
            return await self.update_docker_resources(
                infrastructure_updated.stack_name,
                infrastructure_updated.project_name,
                infrastructure_updated.location,
                event.image_name,
                event.image_version,
                event.image_url,
            )

    async def update_docker_resources(
        self,
        stackName: str,
        projectName: str,
        location: str,
        imageName: str,
        imageVersion: str,
        imageUrl: str = None,
    ) -> List[Event]:
        """
        Updates the docker resources.
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
        :return: A list of events.
        :rtype: pythoneda.shared.Event
        """
        factory = Ports.instance().resolve_first(StackFactory)
        stack = factory.new(stackName, projectName, location)
        return await stack.up_docker_resources(imageName, imageVersion, imageUrl)

    @classmethod
    @listen(InfrastructureRemovalRequested)
    async def listen_InfrastructureRemovalRequested(
        cls, event: InfrastructureRemovalRequested
    ) -> List[Event]:
        """
        Gets notified of a InfrastructureRemovalRequested event.
        :param event: The event.
        :type event: org.acmsl.iac.licdata.domain.InfrastructureRemovalRequested
        :return: A list of events.
        :rtype: List[org.acmsl.iac.licdata.domain.Event]
        """
        cls.instance().add_event(event)
        cls.logger().info(
            f"Infrastructure removal for {event.project_name}/{event.stack_name} at {event.location} requested"
        )
        followUp = await cls.instance().remove_infrastructure(
            event.stack_name, event.project_name, event.location
        )
        for event in followUp:
            cls.instance().add_event(event)
        result = followUp
        return result

    async def remove_infrastructure(
        self, stackName: str, projectName: str, location: str
    ) -> List[Event]:
        """
        Removes the infrastructure.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The location.
        :type location: str
        :return: A list of events.
        :rtype: pythoneda.shared.Event
        """
        factory = Ports.instance().resolve_first(StackFactory)
        stack = factory.new(stackName, projectName, location)
        return await stack.destroy()


# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

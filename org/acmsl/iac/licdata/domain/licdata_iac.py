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
from pythoneda.shared import Event, EventEmitter, EventListener, Flow, listen, Ports
from pythoneda.shared.artifact.events import DockerImagePushed
from pythoneda.shared.iac.events import (
    DockerImageDetailsRequested,
    DockerResourcesRemovalRequested,
    DockerResourcesRemoved,
    DockerResourcesUpdateRequested,
    DockerResourcesUpdated,
    InfrastructureRemovalRequested,
    InfrastructureRemoved,
    InfrastructureUpdateRequested,
    InfrastructureUpdated,
)
from pythoneda.shared.iac import StackOperationFactory
from pythoneda.shared.runtime.secrets.events import CredentialIssued
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
        return await cls.instance().update_infrastructure(event)

    async def update_infrastructure(
        self, event: InfrastructureUpdateRequested
    ) -> List[Event]:
        """
        Updates the infrastructure.
        :param event: The event.
        :type event: org.acmsl.iac.licdata.domain.InfrastructureUpdateRequested
        :return: A list of events.
        :rtype: pythoneda.shared.Event
        """
        factory = Ports.instance().resolve_first(StackOperationFactory)
        stack_operation = factory.new(event)
        followUp = await stack_operation.perform()
        result = followUp
        if len(followUp) > 0 and not followUp[-1].is_error:
            credentials = (
                await stack_operation.retrieve_container_registry_credentials()
            )
            prev_event = followUp[-1]
            credential_issued = CredentialIssued(
                credentials.get("credential_name", None),
                credentials.get("credential_password", None),
                {
                    "stack_name": event.stack_name,
                    "project_name": event.project_name,
                    "location": event.location,
                    "docker_registry_url": credentials.get("docker_registry_url", None),
                },
                [prev_event.id] + prev_event.previous_event_ids,
            )
            result.append(credential_issued)

        for evt in result:
            self.add_event(evt)

        return result

    @classmethod
    @listen(CredentialIssued)
    async def listen_CredentialIssued(cls, event: CredentialIssued) -> List[Event]:
        """
        Gets notified of a CredentialIssued event.
        :param event: The event.
        :type event: pythoneda.shared.runtime.secrets.events.CredentialIssued
        :return: The resulting events.
        :rtype: List[pythoneda.shared.Event]
        """
        cls.instance().add_event(event)
        return await cls.instance().resume(event)

    @classmethod
    @listen(DockerImagePushed)
    async def listen_DockerImagePushed(cls, event: DockerImagePushed) -> List[Event]:
        """
        Gets notified of a DockerImagePushed event.
        :param event: The event.
        :type event: pythoneda.shared.artifact.events.DockerImagePushed
        :return: The resulting events.
        :rtype: List[Event]
        """
        cls.instance().add_event(event)
        return await cls.instance().resume(event)

    async def continue_flow(self, event: Event) -> List[Event]:
        """
        Continues the flow with a new event.
        :param event: The event.
        :type event: pythoneda.shared.Event
        :return: The resulting events.
        :rtype: List[Event]
        """
        result = []
        if isinstance(event, CredentialIssued):
            result = await self.continue_flow_after_CredentialIssued(event)
        elif isinstance(event, DockerImagePushed):
            result = await self.continue_flow_after_DockerImagePushed(event)
        else:
            result = None

        for new_event in result:
            self.add_event(new_event)

        return result

    async def continue_flow_after_CredentialIssued(self, event: Event):
        """
        Continues the flow with a new event.
        :param event: The event.
        :type event: pythoneda.shared.Event
        :return: The resulting events.
        :rtype: List[pythoneda.shared.Event]
        """
        infrastructure_updated = self.find_latest_event(InfrastructureUpdated)
        if infrastructure_updated is None:
            LicdataIac.logger().error(
                f"Could not find the previous InfrastructureUpdated event"
            )
        else:
            metadata = {
                "credential_name": infrastructure_updated.metadata.get(
                    "credential_name", None
                ),
                "docker_registry_url": infrastructure_updated.metadata.get(
                    "docker_registry_url", None
                ),
            }
            factory = Ports.instance().resolve_first(StackOperationFactory)
            docker_image_details_requested = DockerImageDetailsRequested(
                infrastructure_updated.stack_name,
                infrastructure_updated.project_name,
                infrastructure_updated.location,
                metadata,
                [event.id] + event.previous_event_ids,
            )
            self.add_event(docker_image_details_requested)
            stack_operation = factory.new(docker_image_details_requested)
            result = await stack_operation.perform()

        if result is not None:
            for event in result:
                self.add_event(event)
        return result

    async def continue_flow_after_DockerImagePushed(self, event: DockerImagePushed):
        """
        Continues the flow with a new DockerImagePushed event.
        :param event: The event.
        :type event: pythoneda.shared.artifact.events.DockerImagePushed
        :return: The resulting events.
        :rtype: List[pythoneda.shared.Event]
        """
        result = []
        infrastructure_updated = self.find_latest_event(InfrastructureUpdated)
        if infrastructure_updated is None:
            LicdataIac.logger().error(
                f"Could not find the previous InfrastructureUpdated event"
            )
        else:
            LicdataIac.logger().info("Requesting update of Docker resources")
            docker_resources_update_requested = DockerResourcesUpdateRequested(
                infrastructure_updated.stack_name,
                infrastructure_updated.project_name,
                infrastructure_updated.location,
                event.image_name,
                event.image_version,
                event.image_url,
                [event.id] + event.previous_event_ids,
            )
            self.add_event(docker_resources_update_requested)
            result = await self.update_docker_resources(
                docker_resources_update_requested
            )
        if result is not None:
            for event in result:
                self.add_event(event)

        return result

    async def update_docker_resources(
        self, event: DockerResourcesUpdateRequested
    ) -> List[Event]:
        """
        Updates the docker resources.
        :param event: The event.
        :type event: pythoneda.shared.iac.events.DockerResourcesUpdateRequested
        :return: A list of events.
        :rtype: pythoneda.shared.Event
        """
        factory = Ports.instance().resolve_first(StackOperationFactory)
        stack_operation = factory.new(event)
        LicdataIac.logger().debug(f"Performing {stack_operation}({event})")
        result = await stack_operation.perform()
        LicdataIac.logger().debug(f"{stack_operation} finished")

        for event in result:
            self.add_event(event)

        return result

    @classmethod
    @listen(InfrastructureRemovalRequested)
    async def listen_InfrastructureRemovalRequested(
        cls, event: InfrastructureRemovalRequested
    ) -> List[Event]:
        """
        Gets notified of a InfrastructureRemovalRequested event.
        :param event: The event.
        :type event: org.acmsl.iac.licdata.domain.InfrastructureRemovalRequested
        :return: The resulting events.
        :rtype: List[pythoneda.shared.Event]
        """
        cls.instance().add_event(event)
        cls.logger().info(
            f"Infrastructure removal for {event.project_name}/{event.stack_name} at {event.location} requested"
        )
        result = await cls.instance().remove_infrastructure(event)
        for event in result:
            cls.instance().add_event(event)
        return result

    async def remove_infrastructure(
        cls, event: InfrastructureRemovalRequested
    ) -> List[Event]:
        """
        Removes the infrastructure.
        :param event: The event.
        :type event: org.acmsl.iac.licdata.domain.InfrastructureRemovalRequested
        :return: The resulting events.
        :rtype: List[pythoneda.shared.Event]
        """
        factory = Ports.instance().resolve_first(StackOperationFactory)
        stack_operation = factory.new(event)
        return await stack_operation.perform()


# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

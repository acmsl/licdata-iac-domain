#!/usr/bin/env python3

import asyncio
from org.acmsl.licdata.iac.domain import LicdataIac, InfrastructureUpdateRequested
from org.acmsl.licdata.iac.application import LicdataIacApp

asyncio.run(
    LicdataIacApp().accept_pulumi_options(
        {"stackName": "dev", "projectName": "licdata-iac", "location": "westeurope"}
    )
)

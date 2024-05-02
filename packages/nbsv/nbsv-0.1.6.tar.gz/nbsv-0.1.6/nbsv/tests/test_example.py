#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Megan Riel-Mehan.
# Distributed under the terms of the Modified BSD License.

import numpy as np
from simulariumio import TrajectoryData, MetaData, AgentData
from ..viewer import ViewerWidget


def test_example_creation():
    trajectory = TrajectoryData(
        meta_data=MetaData(
            box_size=np.array([10.0, 10.0, 10.0]),
        ),
        agent_data=AgentData(
            times=[0.0],
            n_agents=[1],
            viz_types=[[1000.0]],
            unique_ids=[[1]],
            types=[['A']],
            positions=[[[0, 0, 0]]],
            radii=[[5]]
        )
    )
    w = ViewerWidget(trajectory)
    assert w.height == 300

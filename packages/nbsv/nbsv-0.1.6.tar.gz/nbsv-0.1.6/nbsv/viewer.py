#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Megan Riel-Mehan.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""
import ipywidgets
import numpy as np
from simulariumio import (
    TrajectoryData,
    TrajectoryConverter,
    AgentData,
    CameraData,
    MetaData,
    ModelMetaData,
    UnitData,
    DisplayData,
)
from traitlets import Unicode, Int, Instance
from typing import List, Dict
from ._frontend import module_name, module_version


@ipywidgets.register
class ViewerWidget(ipywidgets.DOMWidget):
    _model_name = Unicode("TrajectoryModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("Viewport").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    trajectory = Instance(TrajectoryData)
    converter = Instance(TrajectoryConverter)
    trajectory_str = Unicode("").tag(sync=True)
    width = Int(500).tag(sync=True)
    height = Int(300).tag(sync=True)

    def __init__(self, trajectory: TrajectoryData, width: int = 500, height: int = 300):
        """
        Simularium viewer widget, to display the requested trajectory
        in a Jupyter notebook

        Parameters
        ----------
        trajectory : TrajectoryData
            Trajectory to display in the simularium viewer widget
        width : int (optional)
            Width of the simularium viewer widget
            Default: 500
        height: int (optional)
            Height of the simularium viewer widget
            Default: 300
        """
        super(ipywidgets.DOMWidget, self).__init__()
        self.width = width
        self.height = height
        self.load_trajectory(trajectory)

    def load_trajectory(self, trajectory: TrajectoryData):
        # Update current trajectory to the provided TrajectoryData object
        self.trajectory = trajectory
        self.converter = TrajectoryConverter(self.trajectory)
        self.trajectory_str = self.converter.to_JSON()

    def update_agent_data(
        self,
        times: np.ndarray = None,
        n_agents: np.ndarray = None,
        viz_types: np.ndarray = None,
        unique_ids: np.ndarray = None,
        types: List = None,
        positions: np.ndarray = None,
        radii: np.ndarray = None,
        rotations: np.ndarray = None,
        n_subpoints: np.ndarray = None,
        subpoints: np.ndarray = None,
        display_data: Dict[str, DisplayData] = None,
    ):
        """
        Update AgentData portion of the TrajectoryData object, overwriting
        original values with values provided as parameters. Parameters that
        are not provided will retain their previous value.

        Parameters
        ----------
        times : np.ndarray (shape = [timesteps]) (optional)
            A numpy ndarray containing the elapsed simulated time at each
            timestep to overwrite the previous AgentData.times
        n_agents : np.ndarray (shape = [timesteps]) (optional)
            A numpy ndarray containing the number of agents that exist at
            each timestep to overwrite the previous AgentData.n_agents
        viz_types : np.ndarray (shape = [timesteps, agents]) (optional)
            A numpy ndarray containing the viz type for each agent at each
            timestep to overwrite the previous AgentData.viz_types.
            Current options:
                1000 : default,
                1001 : fiber (which will require subpoints)
        unique_ids : np.ndarray (shape = [timesteps, agents]) (optional)
            A numpy ndarray containing the unique ID for each agent at each
            timestep to overwrite the previous AgentData.unique_ids.
        types : List[List[str]] (list of shape [timesteps, agents]) (optional)
            A list containing timesteps, for each a list of the string name
            for the type of each agent to overwrite the previous AgentData.types
        positions : np.ndarray (shape = [timesteps, agents, 3]) (optional)
            A numpy ndarray containing the XYZ position for each agent at
            each timestep to overwrite the previous AgentData.positions
        radii : np.ndarray (shape = [timesteps, agents]) (optional)
            A numpy ndarray containing the radius for each agent at each
            timestep to overwrite the previous AgentData.radii
        rotations : np.ndarray  (shape = [timesteps, agents, 3]) (optional)
            A numpy ndarray containing the XYZ euler angles representing
            the rotation for each agent at each timestep in degrees to
            overwrite the previous AgentData.rotations
        n_subpoints : np.ndarray (shape = [timesteps, agents]) (optional)
            A numpy ndarray containing the number of subpoints
            belonging to each agent at each timestep. Will overwrite the previous
            AgentData.n_subpoints, only required if subpoints are provided
        subpoints : np.ndarray (shape = [timesteps, agents, subpoints]) (optional)
            A numpy ndarray containing a list of subpoint data for each agent at
            each timestep. Will to overwrite the previous AgentData.subpoints, only
            used for fiber and sphere group agent types
        display_data: Dict[str,DisplayData] (optional)
            A dictionary mapping agent type name to DisplayData to use for
            that type, will overwrite the previous AgentData.display_data
        """
        new_agent_data = AgentData(
            times=times if times is not None else self.trajectory.agent_data.times,
            n_agents=(
                n_agents
                if n_agents is not None
                else self.trajectory.agent_data.n_agents
            ),
            viz_types=(
                viz_types
                if viz_types is not None
                else self.trajectory.agent_data.viz_types
            ),
            unique_ids=(
                unique_ids
                if unique_ids is not None
                else self.trajectory.agent_data.unique_ids
            ),
            types=types if types is not None else self.trajectory.agent_data.types,
            positions=(
                positions
                if positions is not None
                else self.trajectory.agent_data.positions
            ),
            radii=radii if radii is not None else self.trajectory.agent_data.radii,
            rotations=(
                rotations
                if rotations is not None
                else self.trajectory.agent_data.rotations
            ),
            n_subpoints=(
                n_subpoints
                if n_subpoints is not None
                else self.trajectory.agent_data.n_subpoints
            ),
            subpoints=(
                subpoints
                if subpoints is not None
                else self.trajectory.agent_data.subpoints
            ),
            display_data=(
                display_data
                if display_data is not None
                else self.trajectory.agent_data.display_data
            ),
        )
        new_traj = TrajectoryData(
            self.trajectory.meta_data,
            new_agent_data,
            self.trajectory.time_units,
            self.trajectory.spatial_units,
        )
        self.load_trajectory(new_traj)

    def add_display_data(self, display_data: Dict[str, DisplayData]):
        """
        Add to the AgentData.display_data dict without deleting the
        previously entries.

        Parameters
        ----------
        display_data: Dict[str,DisplayData]
            A dictionary mapping agent type name to DisplayData to use for
            that type, to be added to the previous AgentData.display_data.
            If this dict has any keys that are present in the previous
            display_data dict, the previous values will be overwritten by
            these newly provided values
        """
        new_agent_data = AgentData(
            times=self.trajectory.agent_data.times,
            n_agents=self.trajectory.agent_data.n_agents,
            viz_types=self.trajectory.agent_data.viz_types,
            unique_ids=self.trajectory.agent_data.unique_ids,
            types=self.trajectory.agent_data.types,
            positions=self.trajectory.agent_data.positions,
            radii=self.trajectory.agent_data.radii,
            rotations=self.trajectory.agent_data.rotations,
            n_subpoints=self.trajectory.agent_data.n_subpoints,
            subpoints=self.trajectory.agent_data.subpoints,
            display_data=self.trajectory.agent_data.display_data.update(display_data),
        )
        new_traj = TrajectoryData(
            self.trajectory.meta_data,
            new_agent_data,
            self.trajectory.time_units,
            self.trajectory.spatial_units,
        )
        self.load_trajectory(new_traj)

    def update_meta_data(
        self,
        box_size: np.ndarray = None,
        camera_position: np.ndarray = None,
        camera_look_at_position: np.ndarray = None,
        camera_up_vector: np.ndarray = None,
        camera_fov_degrees: float = None,
        scale_factor: float = None,
        trajectory_title: str = None,
        title: str = None,
        version: str = None,
        authors: str = None,
        description: str = None,
        source_code_url: str = None,
        input_data_url: str = None,
        raw_output_data_url: str = None,
    ):
        """
        Update MetaData portion of the TrajectoryData object, overwriting
        original values with values provided as parameters. Parameters that
        are not provided will retain their previous value.

        Parameters
        ----------
        box_size : np.ndarray (shape = [3]) (optional)
            A numpy ndarray containing the XYZ dimensions of the simulation
            bounding volume to overwrite the previous
            TrajectoryData.meta_data.box_size
        camera_position :  np.ndarray (shape = [3]) (optional)
            3D position of the camera itself, to overwrite the previous
            TrajectoryData.meta_data.camera_defaults.position
        camera_look_at_position :  np.ndarray (shape = [3]) (optional)
            position the camera looks at, to overwrite the previous
            TrajectoryData.meta_data.camera_defaults.look_at_position
        camera_up_vector :  np.ndarray (shape = [3]) (optional)
            the vector that defines which direction is "up" in the
            camera's view, to overwrite the previous
            TrajectoryData.meta_data.camera_defaults.up_vector
        camera_fov_degrees : float (optional)
            the angle defining the extent of the 3D world that is seen
            from bottom to top of the camera view, to overwrite the previous
            TrajectoryData.meta_data.camera_defaults.fov_degrees
        scale_factor :  float (optional)
            A multiplier for the scene, use if visualization is too large or
            small, to overwrite the previous TrajectoryData.meta_data.scale_factor
        trajectory_title : str (optional)
            A title for this run of the model, to overwrite the previous
            TrajectoryData.meta_data.trajectory_title
        title : str (optional)
            Display title for this model, to overwrite the previous
            TrajectoryData.meta_data.model_meta_data.title
        version : str (optional)
            Version number of the model that produced this trajectory, to overwrite
            the previous TrajectoryData.meta_data.model_meta_data.version
        authors : str (optional)
            Modelers name(s), to overwrite the previous
            TrajectoryData.meta_data.model_meta_data.authors
        description : str (optional)
            Comments to display with the trajectories generated by this model,
            to overwrite the previous
            TrajectoryData.meta_data.model_meta_data.description
        doi : str (optional)
            The DOI of the publication accompanying this model, to overwrite the
            previous TrajectoryData.meta_data.model_meta_data.doi
        source_code_url : str (optional)
            If the code that generated this model is posted publicly, a link to
            the repository of source code, to overwrite the previous
            TrajectoryData.meta_data.model_meta_data.source_code_url
        source_code_license_url : str (optional)
            A link to the license for the source code, to overwrite the previous
            TrajectoryData.meta_data.model_meta_data.source_code_license_url
        input_data_url : str (optional)
            A link to any model configuration or parameter files posted
            publicly, to overwrite the previous
            TrajectoryData.meta_data.model_meta_data.input_data_url
        raw_output_data_url : str (optional)
            A link to any raw outputs from the source code posted
            publicly, to overwrite the previous
            TrajectoryData.meta_data.model_meta_data.raw_output_data_url
        """
        new_camera_defaults = CameraData(
            position=(
                camera_position
                if camera_position is not None
                else self.trajectory.meta_data.camera_defaults.position
            ),
            look_at_position=(
                camera_look_at_position
                if camera_look_at_position is not None
                else self.trajectory.meta_data.camera_defaults.look_at_position
            ),
            up_vector=(
                camera_up_vector
                if camera_up_vector is not None
                else self.trajectory.meta_data.camera_defaults.up_vector
            ),
            fov_degrees=(
                camera_fov_degrees
                if camera_fov_degrees is not None
                else self.trajectory.meta_data.camera_defaults.fov_degrees
            ),
        )
        new_model_metadata = ModelMetaData(
            title=(
                title
                if title is not None
                else self.trajectory.meta_data.model_meta_data.title
            ),
            version=(
                version
                if version is not None
                else self.trajectory.meta_data.model_meta_data.version
            ),
            authors=(
                authors
                if authors is not None
                else self.trajectory.meta_data.model_meta_data.authors
            ),
            description=(
                description
                if description is not None
                else self.trajectory.meta_data.model_meta_data.description
            ),
            source_code_url=(
                source_code_url
                if source_code_url is not None
                else self.trajectory.meta_data.model_meta_data.source_code_url
            ),
            input_data_url=(
                input_data_url
                if input_data_url is not None
                else self.trajectory.meta_data.model_meta_data.input_data_url
            ),
            raw_output_data_url=(
                raw_output_data_url
                if raw_output_data_url is not None
                else self.trajectory.meta_data.model_meta_data.raw_output_data_url
            ),
        )
        new_metadata = MetaData(
            box_size=(
                box_size if box_size is not None else self.trajectory.meta_data.box_size
            ),
            camera_defaults=new_camera_defaults,
            scale_factor=(
                scale_factor
                if scale_factor is not None
                else self.trajectory.meta_data.scale_factor
            ),
            trajectory_title=(
                trajectory_title
                if trajectory_title is not None
                else self.trajectory.meta_data.trajectory_title
            ),
            model_meta_data=new_model_metadata,
        )
        new_traj = TrajectoryData(
            new_metadata,
            self.trajectory.agent_data,
            self.trajectory.time_units,
            self.trajectory.spatial_units,
        )
        self.load_trajectory(new_traj)

    def update_time_units(
        self,
        name: str = None,
        magnitude: float = None,
    ):
        """
        Update time_units UnitData portion of the TrajectoryData object,
        overwriting original values with those provided as parameters.
        Parameters that are not provided will retain their previous value.

        Parameters
        ----------
        name: str
            unit name for values (we support this list
            https://github.com/hgrecco/pint/blob/master/pint/default_en.txt),
            to overwrite the previous TrajectoryData.time_units.name
        magnitude: float (optional)
            multiplier for values (in case they are not given in whole units),
            to overwrite the previous TrajectoryData.time_units.magnitude
        """
        new_time_units = UnitData(
            name=name if name is not None else self.trajectory.time_units.name,
            magnitude=(
                magnitude
                if magnitude is not None
                else self.trajectory.time_units.magnitude
            ),
        )
        new_traj = TrajectoryData(
            self.trajectory.meta_data,
            self.trajectory.agent_data,
            new_time_units,
            self.trajectory.spatial_units,
        )
        self.load_trajectory(new_traj)

    def update_spatial_units(
        self,
        name: str = None,
        magnitude: float = None,
    ):
        """
        Update spatial_units UnitData portion of the TrajectoryData object,
        overwriting original values with those provided as parameters.
        Parameters that are not provided will retain their previous value.

        Parameters
        ----------
        name: str
            unit name for values (we support this list
            https://github.com/hgrecco/pint/blob/master/pint/default_en.txt),
            to overwrite the previous TrajectoryData.spatial_units.name
        magnitude: float (optional)
            multiplier for values (in case they are not given in whole units),
            to overwrite the previous TrajectoryData.spatial_units.magnitude
        """
        new_spatial_units = UnitData(
            name=name if name is not None else self.trajectory.spatial_units.name,
            magnitude=(
                magnitude
                if magnitude is not None
                else self.trajectory.spatial_units.magnitude
            ),
        )
        new_traj = TrajectoryData(
            self.trajectory.meta_data,
            self.trajectory.agent_data,
            self.trajectory.time_units,
            new_spatial_units,
        )
        self.load_trajectory(new_traj)

    def save(self, file_name: str):
        """
        Save simularium trajectory currently represented in the widget
        locally at the provided file name .simularium

        Parameters:
         ----------
        name: str
            File name for trajectory to be saved at. No need to include the
            .simularium extension in the name, that will be added automatically
        """
        self.converter.save(file_name)

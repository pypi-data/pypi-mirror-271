// Copyright (c) Megan Riel-Mehan
// Distributed under the terms of the Modified BSD License.
import {
  loadSimulariumFile,
  SimulariumController,
} from '@aics/simularium-viewer';
import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';
import React from 'react';
import ReactDOM from 'react-dom';

import { MODULE_NAME, MODULE_VERSION } from './version';
import Viewer, { ViewerProps } from './Viewer';

// Import the CSS
import '../css/widget.css';
import { VisibilityProvider } from './AgentVisibilityContext';
import StyleProvider from './ConfigProvider';

const defaultModelProperties = {
  trajectory: '',
  width: 400,
  height: 400,
};

// const netConnectionSettings = {
//   serverIp: 'production-node1-agentviz-backend.cellexplore.net',
//   serverPort: 9002,
// };

export type WidgetModelState = typeof defaultModelProperties;

export class TrajectoryModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),

      _model_name: TrajectoryModel.model_name,
      _model_module: TrajectoryModel.model_module,
      _model_module_version: TrajectoryModel.model_module_version,
      _view_name: TrajectoryModel.view_name,
      _view_module: TrajectoryModel.view_module,
      _view_module_version: TrajectoryModel.view_module_version,
      ...defaultModelProperties,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'TrajectoryModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'Viewport'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class Viewport extends DOMWidgetView {
  controller: SimulariumController;
  async initialize(): Promise<void> {
    this.controller = new SimulariumController({});
    await this.trajectory_changed();
  }

  render(): void {
    this.el.classList.add('custom-widget');
    const wrappedComponent = React.createElement(
      StyleProvider,
      null,
      React.createElement(
        VisibilityProvider,
        null,
        React.createElement(Viewer, {
          controller: this.controller,
        } as ViewerProps)
      )
    );

    ReactDOM.render(wrappedComponent, this.el);
  }

  async trajectory_changed(): Promise<void> {
    const controller = this.controller;
    const trajectory_as_string = this.model.get('trajectory_str');
    if (!trajectory_as_string) {
      return;
    }
    const blob = new Blob([trajectory_as_string], { type: 'application/json' });
    const simulariumFile = await loadSimulariumFile(blob);
    await controller.changeFile({ simulariumFile }, 'test.siumularium');
  }
}

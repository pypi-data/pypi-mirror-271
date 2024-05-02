import * as React from 'react';
import { ModelInfo } from '@aics/simularium-viewer/type-declarations/simularium/types';

import '../../css/model_display_data.css';

interface ModelDisplayDataProps extends ModelInfo {
  trajectoryTitle?: string;
}

const ModelDisplayData: React.FunctionComponent<ModelDisplayDataProps> = (
  props: ModelDisplayDataProps
): JSX.Element => {
  const { title, trajectoryTitle } = props;

  return (
    <div className="model-display-data-container">
      {trajectoryTitle || title || '<Untitled trajectory>'}
    </div>
  );
};

export default ModelDisplayData;

import * as React from 'react';

import { ScaleBarIcon } from './Icons';

import '../../css/scale_bar.css';

interface ScaleBarProps {
  label: string;
}

const ScaleBar = (scaleBarProps: ScaleBarProps): JSX.Element => {
  const { label } = scaleBarProps;
  const scaleBarNode = label ? (
    <div className="scale-bar">
      {label}
      {ScaleBarIcon}
    </div>
  ) : (
    <div />
  );

  return scaleBarNode;
};
export default ScaleBar;

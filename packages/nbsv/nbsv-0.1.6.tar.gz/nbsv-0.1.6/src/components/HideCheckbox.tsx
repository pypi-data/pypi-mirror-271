import React from 'react';
import { Checkbox, Tooltip } from 'antd';

import { CheckboxProps } from '../types';
import { CheckboxState, TOOLTIP_COLOR, tooltipMap } from '../constants';

const HideCheckbox: React.FunctionComponent<CheckboxProps> = (
  props: CheckboxProps
): JSX.Element => {
  const { agent, selections, clickHandler } = props;

  const maxSelections =
    agent.displayStates.length > 0 ? agent.displayStates.length : 1;

  const getCheckboxStatus = () => {
    if (selections.length === 0) {
      return CheckboxState.Checked;
    }
    if (selections.length === maxSelections) {
      return CheckboxState.Unchecked;
    }
    return CheckboxState.Indeterminate;
  };

  const checkboxStatus = getCheckboxStatus();
  const tooltipText = tooltipMap[checkboxStatus];

  return (
    <Tooltip
      placement="right"
      title={tooltipText}
      color={TOOLTIP_COLOR}
      trigger={['focus', 'hover']}
    >
      <Checkbox
        indeterminate={checkboxStatus === 'Indeterminate'}
        checked={checkboxStatus === 'Checked'}
        onClick={clickHandler}
      />
    </Tooltip>
  );
};

export default HideCheckbox;

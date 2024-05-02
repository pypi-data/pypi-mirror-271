import React from 'react';
import { Checkbox, Tooltip } from 'antd';

import { ChildCheckboxProps } from '../types';
import { CheckboxState, TOOLTIP_COLOR, tooltipMap } from '../constants';

const ChildHideCheckbox: React.FunctionComponent<ChildCheckboxProps> = (
  props: ChildCheckboxProps
): JSX.Element => {
  const { name, selections, clickHandler } = props;

  const getCheckboxStatus = () => {
    if (selections.includes(name)) {
      return CheckboxState.Unchecked;
    }
    return CheckboxState.Checked;
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
      <Checkbox checked={checkboxStatus === 'Checked'} onClick={clickHandler} />
    </Tooltip>
  );
};

export default ChildHideCheckbox;

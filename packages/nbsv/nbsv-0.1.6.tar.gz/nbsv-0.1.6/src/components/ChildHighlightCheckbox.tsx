import React from 'react';
import { Tooltip } from 'antd';

import { CheckboxState, TOOLTIP_COLOR } from '../constants';
import { ChildCheckboxProps, HighlightDisplayOption } from '../types';
import {
  HighlightStar,
  IndeterminateHighlightStar,
  NoHighlightStar,
} from './Icons';

const ChildHighlightCheckbox: React.FunctionComponent<ChildCheckboxProps> = (
  props: ChildCheckboxProps
): JSX.Element => {
  const { name, selections, clickHandler } = props;

  const getCheckboxStatus = () => {
    if (selections.includes(name)) {
      return CheckboxState.Checked;
    }
    return CheckboxState.Unchecked;
  };

  const getHighlightDisplayOptions = (
    checkboxStatus: CheckboxState
  ): HighlightDisplayOption => {
    switch (checkboxStatus) {
      case CheckboxState.Checked:
        return {
          tooltipText: 'Remove highlight',
          ariaLabel: 'true',
          icon: HighlightStar,
        };
      case CheckboxState.Unchecked:
        return {
          tooltipText: 'Highlight',
          ariaLabel: 'false',
          icon: NoHighlightStar,
        };
      case CheckboxState.Indeterminate:
        return {
          tooltipText: 'Highlight',
          ariaLabel: 'mixed',
          icon: IndeterminateHighlightStar,
        };
    }
  };

  const checkboxStatus = getCheckboxStatus();
  const { tooltipText, ariaLabel, icon } =
    getHighlightDisplayOptions(checkboxStatus);

  return (
    <Tooltip
      placement="top"
      title={tooltipText}
      color={TOOLTIP_COLOR}
      trigger={['focus', 'hover']}
    >
      <input
        type="checkbox"
        aria-label={ariaLabel}
        tabIndex={0}
        style={{
          position: 'absolute',
          opacity: 0,
          cursor: 'pointer',
        }}
        onClick={clickHandler}
      />
      <label style={{ fill: '#d3d3d3' }}>{icon}</label>
    </Tooltip>
  );
};

export default ChildHighlightCheckbox;

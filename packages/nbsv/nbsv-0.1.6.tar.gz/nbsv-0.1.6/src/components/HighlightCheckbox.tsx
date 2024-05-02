import React from 'react';
import { Tooltip } from 'antd';

import { CheckboxState, TOOLTIP_COLOR } from '../constants';
import { CheckboxProps, HighlightDisplayOption } from '../types';
import {
  HighlightStar,
  IndeterminateHighlightStar,
  NoHighlightStar,
} from './Icons';

const HighlightCheckbox: React.FunctionComponent<CheckboxProps> = (
  props: CheckboxProps
): JSX.Element => {
  const { agent, selections, clickHandler } = props;

  const maxSelections =
    agent.displayStates.length > 0 ? agent.displayStates.length : 1;

  const getCheckboxStatus = () => {
    if (selections.length === 0) {
      return CheckboxState.Unchecked;
    }
    if (selections.length === maxSelections) {
      return CheckboxState.Checked;
    }
    return CheckboxState.Indeterminate;
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

export default HighlightCheckbox;

export const agentColors = [
  '#fee34d',
  '#f7b232',
  '#bf5736',
  '#94a7fc',
  '#ce8ec9',
  '#58606c',
  '#0ba345',
  '#9267cb',
  '#81dbe6',
  '#bd7800',
  '#bbbb99',
  '#5b79f0',
  '#89a500',
  '#da8692',
  '#418463',
  '#9f516c',
  '#00aabf',
];

export const TOOLTIP_COLOR = '#3B3649';

export const SIDE_PANEL_WIDTH: number = 280;
export const MIN_WIDTH_TO_SHOW_SIDE_PANEL: number = 580;
export const VIEWER_INITIAL_WIDTH: number = 500;
export const VIEWER_HEIGHT: number = 580;

/**
 * A UserChangesMap stores user changes to highlighting and hiding (made by clicking checkboxes).
 * There should be a key in the map for each agent name,
 * and the value is an array to hold user changes to selection: hiding and highlighting.
 * The default state of the value array is to be empty.
 * If an agent with no display states is hidden or highlighted, the array will contain the agent name.
 * If an agent has display states, those states that are hidden/highlighted will be in the array.
 * userChangesMap[agentName] = [] means nothing is hidden/highlighted
 * userChangesMap[agentName] = [agentName] means the agent is hidden/highlighted in a case with no display states
 * userChangesMap[agentName] = [displayState1, displayState2] means whatever display states are in the array are hidden/highlighted
 */
export interface UserChangesMap {
  [key: string]: string[];
}

export enum CheckboxState {
  Checked = 'Checked',
  Unchecked = 'Unchecked',
  Indeterminate = 'Indeterminate',
}

export const tooltipMap = {
  [CheckboxState.Checked]: 'Hide',
  [CheckboxState.Unchecked]: 'Show',
  [CheckboxState.Indeterminate]: 'Show',
};

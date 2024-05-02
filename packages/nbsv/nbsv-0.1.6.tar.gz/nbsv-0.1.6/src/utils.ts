import { SelectionEntry, UIDisplayData } from '@aics/simularium-viewer';
import { UserChangesMap } from './constants';
import { UIDisplayEntry } from '@aics/simularium-viewer/type-declarations/simularium/SelectionInterface';

export const updateUserChangesAfterCheckboxClick = (
  name: string,
  children: string[],
  currentUserChanges: UserChangesMap
): UserChangesMap => {
  const newMap: UserChangesMap = { ...currentUserChanges };
  // for a checkbox with no children, this is just the agent name
  // for a checkbox with children it is an array of all the children
  const allPossibleCheckboxes = children.length === 0 ? [name] : children;
  // if they aren't currently all on, we turn them all on
  if (currentUserChanges[name].length !== allPossibleCheckboxes.length) {
    newMap[name] = allPossibleCheckboxes;
  } else {
    newMap[name] = [];
  }
  return newMap;
};

export const getSelectionAfterChildCheckboxClick = (
  name: string,
  parent: string,
  currentUserChanges: UserChangesMap
): UserChangesMap => {
  const newMap: UserChangesMap = { ...currentUserChanges };
  const currentChildren = newMap[parent];
  // Shouldn't ever hit this conditional, userChangesMap was not made correctly if so
  if (currentChildren === undefined) {
    throw new Error('Parent not found in map');
  }
  // toggles inclusion in the array
  const updatedChildren = currentChildren.includes(name)
    ? currentChildren.filter((child) => child !== name)
    : [...currentChildren, name];

  newMap[parent] = updatedChildren;
  return newMap;
};

export const getChildren = (agent: UIDisplayEntry): string[] => {
  if (agent.displayStates.length === 0) {
    return [];
  }
  return agent.displayStates.map((state) => state.id);
};

export const convertMapToSelectionStateInfo = (
  currentUserChangesMap: UserChangesMap,
  uiData: UIDisplayData
): SelectionEntry[] => {
  const init: SelectionEntry[] = [];
  return uiData.reduce((acc, agent) => {
    // Theoretically, this block should never be hit because `agentVisibilityMap`
    // should always contain all the agents in `agentDisplayData`
    if (!currentUserChangesMap[agent.name]) {
      return acc;
    }
    const selectedTags = currentUserChangesMap[agent.name];
    if (selectedTags.length === 1 && selectedTags[0] === agent.name) {
      // if an agent with no display states is selected we make a selection entry for it
      acc.push({
        name: agent.name,
        tags: [],
      });
    } else if (selectedTags.length > 0) {
      // if an agent with display states has some or all states selected we make a selection entry for it
      acc.push({
        name: agent.name,
        tags: selectedTags,
      });
    }
    return acc;
  }, init);
};

export const makeEmptyUserSelections = (uiDisplayData: UIDisplayData) => {
  return uiDisplayData.reduce<UserChangesMap>((acc, agent) => {
    acc[agent.name] = [];
    return acc;
  }, {});
};

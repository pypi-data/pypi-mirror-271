import React, { createContext, useState, ReactNode } from 'react';
import { UIDisplayData } from '@aics/simularium-viewer';

import { UserChangesMap } from './constants';
import {
  makeEmptyUserSelections,
  updateUserChangesAfterCheckboxClick,
  getSelectionAfterChildCheckboxClick,
} from './utils';

interface VisibilityContextType {
  uiDisplayData: UIDisplayData;
  hiddenAgents: UserChangesMap;
  highlightedAgents: UserChangesMap;
  receiveUIDisplayData: (data: UIDisplayData) => void;
  setHiddenAgents: React.Dispatch<React.SetStateAction<UserChangesMap>>;
  handleHideCheckboxChange: (name: string, children: string[]) => void;
  handleHideChildCheckboxChange: (name: string, parent: string) => void;
  handleHighlightChange: (name: string, children: string[]) => void;
  handleChildHighlightChange: (name: string, parent: string) => void;
}

export const VisibilityContext = createContext<VisibilityContextType>({
  uiDisplayData: [],
  hiddenAgents: {},
  highlightedAgents: {},
  receiveUIDisplayData: () => {},
  setHiddenAgents: () => {},
  handleHideCheckboxChange: () => {},
  handleHideChildCheckboxChange: () => {},
  handleHighlightChange: () => {},
  handleChildHighlightChange: () => {},
});

export const VisibilityProvider = ({ children }: { children: ReactNode }) => {
  const [uiDisplayData, setUiDisplayData] = useState<UIDisplayData>([]);
  const [hiddenAgents, setHiddenAgents] = useState<UserChangesMap>({});
  const [highlightedAgents, setHighlightedAgents] = useState<UserChangesMap>(
    {}
  );

  const receiveUIDisplayData = (data: UIDisplayData) => {
    setUiDisplayData(data);
    setHighlightedAgents(makeEmptyUserSelections(data));
    setHiddenAgents(makeEmptyUserSelections(data));
  };

  const handleHideCheckboxChange = (name: string, children: string[]) => {
    setHiddenAgents((prevHiddenAgents) =>
      updateUserChangesAfterCheckboxClick(name, children, prevHiddenAgents)
    );
  };

  const handleHideChildCheckboxChange = (name: string, parent: string) => {
    setHiddenAgents((prevHiddenAgents) =>
      getSelectionAfterChildCheckboxClick(name, parent, prevHiddenAgents)
    );
  };

  const handleHighlightChange = (name: string, children: string[]) => {
    setHighlightedAgents((prevHighlightedAgents) =>
      updateUserChangesAfterCheckboxClick(name, children, prevHighlightedAgents)
    );
  };

  const handleChildHighlightChange = (name: string, parent: string) => {
    setHighlightedAgents((prevHighlightedAgents) =>
      getSelectionAfterChildCheckboxClick(name, parent, prevHighlightedAgents)
    );
  };

  const vis = {
    uiDisplayData,
    hiddenAgents,
    highlightedAgents,
    receiveUIDisplayData,
    setHiddenAgents,
    handleHighlightChange,
    handleChildHighlightChange,
    handleHideCheckboxChange,
    handleHideChildCheckboxChange,
  };

  return (
    <VisibilityContext.Provider value={vis}>
      {children}
    </VisibilityContext.Provider>
  );
};

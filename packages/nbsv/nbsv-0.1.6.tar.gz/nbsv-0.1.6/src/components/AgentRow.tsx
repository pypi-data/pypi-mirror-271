import React, { useContext } from 'react';
import { UIDisplayEntry } from '@aics/simularium-viewer/type-declarations/simularium/SelectionInterface';

import HideCheckbox from './HideCheckbox';
import HighlightCheckbox from './HighlightCheckbox';
import { CaretDown, CaretRight } from './Icons';
import ChildHideCheckbox from './ChildHideCheckbox';
import ChildHighlightCheckbox from './ChildHighlightCheckbox';
import { VisibilityContext } from '../AgentVisibilityContext';
import { getChildren } from '../utils';

import '../../css/agent_row.css';

interface AgentRowProps {
  agent: UIDisplayEntry;
}

const AgentRow: React.FC<AgentRowProps> = (
  props: AgentRowProps
): JSX.Element => {
  const { agent } = props;

  const {
    handleHideCheckboxChange,
    handleHideChildCheckboxChange,
    handleHighlightChange,
    handleChildHighlightChange,
    highlightedAgents,
    hiddenAgents,
  } = useContext(VisibilityContext);
  const highlightSelections = highlightedAgents[agent.name] || [];
  const hiddenSelections = hiddenAgents[agent.name] || [];

  const [showChildren, setShowChildren] = React.useState(false);
  const hasChildren = agent.displayStates.length > 0;

  const Caret = () => (
    <div
      className="caret-spacer"
      onClick={() => setShowChildren(!showChildren)}
    >
      {showChildren ? CaretDown : CaretRight}
    </div>
  );

  const Spacer = () => <div className="caret-spacer" />;

  const getChildRows = (agent: UIDisplayEntry) => {
    return agent.displayStates.map((displayState) => {
      return (
        <div className="item-row" style={{ display: 'flex' }}>
          <Spacer />
          <ChildHighlightCheckbox
            name={displayState.name}
            selections={highlightSelections}
            clickHandler={() => {
              handleChildHighlightChange(displayState.name, agent.name);
            }}
          />
          <div
            className={['color-swatch', 'child'].join(' ')}
            style={{
              backgroundColor: displayState.color,
            }}
          ></div>
          <ChildHideCheckbox
            name={displayState.name}
            selections={hiddenSelections}
            clickHandler={() =>
              handleHideChildCheckboxChange(displayState.name, agent.name)
            }
          />
          <span>{displayState.name}</span>
        </div>
      );
    });
  };

  const childRows = hasChildren && getChildRows(agent);
  const children = getChildren(agent);

  return (
    <div>
      <div className="item-row">
        {hasChildren ? <Caret /> : <Spacer />}
        <HighlightCheckbox
          agent={agent}
          selections={highlightSelections}
          clickHandler={() => handleHighlightChange(agent.name, children)}
        />
        <div
          className="color-swatch"
          style={{
            backgroundColor: agent.color,
          }}
        ></div>
        <HideCheckbox
          agent={agent}
          selections={hiddenSelections}
          clickHandler={() => handleHideCheckboxChange(agent.name, children)}
        />
        <span>{agent.name}</span>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
        {showChildren && childRows}
      </div>
    </div>
  );
};

export default AgentRow;

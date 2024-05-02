import React, { useContext } from 'react';

import { VisibilityContext } from '../AgentVisibilityContext';
import { VIEWER_HEIGHT } from '../constants';
import AgentRow from './AgentRow';
import HideAllAgentsCheckbox from './HideAllAgentsCheckbox';

import '../../css/side_panel.css';

const SidePanel: React.FC = (): JSX.Element => {
  const { uiDisplayData } = useContext(VisibilityContext);

  return (
    <div className="sp-container" style={{ maxHeight: VIEWER_HEIGHT }}>
      <div className="agent-title">Agents</div>
      <div className={['item-row', 'hide-all'].join(' ')}>
        <HideAllAgentsCheckbox />
        <span>All agent types</span>
      </div>
      {uiDisplayData.map((agent) => (
        <AgentRow key={agent.name} agent={agent} />
      ))}
    </div>
  );
};

export default SidePanel;

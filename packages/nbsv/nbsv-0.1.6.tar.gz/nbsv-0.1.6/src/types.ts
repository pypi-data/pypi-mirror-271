import { UIDisplayEntry } from '@aics/simularium-viewer/type-declarations/simularium/SelectionInterface';

export interface TimeUnits {
  magnitude: number;
  name: string;
}

export interface PlaybackState {
  currentTime: number;
  isPlaying: boolean;
}

export interface PlaybackData {
  timeStep: number;
  lastFrameTime: number;
  firstFrameTime: number;
  timeUnits: TimeUnits;
}

export interface HighlightDisplayOption {
  tooltipText: string;
  ariaLabel: 'true' | 'false' | 'mixed';
  icon: JSX.Element;
}

export interface ChildCheckboxProps {
  name: string;
  selections: string[];
  clickHandler: () => void;
}

export interface CheckboxProps {
  agent: UIDisplayEntry;
  selections: string[];
  clickHandler: () => void;
}

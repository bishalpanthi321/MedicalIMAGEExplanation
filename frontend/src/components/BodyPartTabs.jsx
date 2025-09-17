import React from 'react';

const BODY_PARTS = [
  'head', 'chest', 'lungs', 'legs', 'ribs', 'abdomen', 'spine', 'pelvis'
];

export default function BodyPartTabs({ selected, onSelect }) {
  return (
    <div className="flex space-x-2 mb-4">
      {BODY_PARTS.map(part => (
        <button
          key={part}
          className={`px-4 py-2 rounded-card border transition-colors ${selected === part ? 'bg-primary text-white' : 'bg-secondary text-primary'}`}
          onClick={() => onSelect(part)}
        >
          {part.charAt(0).toUpperCase() + part.slice(1)}
        </button>
      ))}
    </div>
  );
}

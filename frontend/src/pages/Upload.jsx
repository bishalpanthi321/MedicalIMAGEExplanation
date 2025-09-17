import React, { useState } from 'react';
import BodyPartTabs from '../components/BodyPartTabs';

export default function Upload() {
  const [selected, setSelected] = useState('chest');
  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Upload Medical Image</h1>
      <BodyPartTabs selected={selected} onSelect={setSelected} />
      <div className="mt-6 bg-white rounded-card shadow p-6">Upload form (placeholder)</div>
    </div>
  );
}

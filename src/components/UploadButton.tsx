import React, { useState } from 'react';

interface UploadButtonProps {
  onImageUpload: (file: File, location: [number, number] | null) => void;
}

export default function UploadButton({ onImageUpload }: UploadButtonProps) {
  const [hover, setHover] = useState(false);

  const baseStyle: React.CSSProperties = {
    position: 'absolute',
    top: 20,
    right: 20,
    zIndex: 1000,
    borderRadius: 4,
    padding: '10px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
    cursor: 'pointer',
    userSelect: 'none',
  };
  
  const defaultStyle: React.CSSProperties = {
    ...baseStyle,
    backgroundColor: '#f0f0f0',
    color: '#000',
  };
  
  const hoverStyle: React.CSSProperties = {
    ...baseStyle,
    backgroundColor: '#636363',
    color: '#fff',
  };
  

  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    navigator.geolocation.getCurrentPosition(
      position => {
        const { latitude, longitude } = position.coords;
        onImageUpload(file, [latitude, longitude]);
      },
      error => {
        alert('Failed to get location: ' + error.message);
        onImageUpload(file, null); // fallback if location fails
      }
    );
  }

  return (
    <div
      style={hover ? hoverStyle : defaultStyle}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
    >
      <label>
        Upload
        <input type="file" accept="image/*" onChange={handleFileChange} style={{ display: 'none' }} />
      </label>
    </div>
  );
}

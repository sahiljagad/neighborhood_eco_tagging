import React from 'react';

interface UploadButtonProps {
  onImageUpload: (file: File, location: [number, number] | null) => void;
}
export default function UploadButton({onImageUpload}: UploadButtonProps) {

  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      navigator.geolocation.getCurrentPosition(position => {
        const { latitude, longitude } = position.coords;
        if (latitude && longitude) {
          onImageUpload(file, [latitude, longitude]);
        } else {
          alert('No GPS data found in this image.');
        }
      });
    } catch (error) {
      console.error('EXIF parsing failed:', error);
    }
  }

  return (
    <div style={{ position: 'absolute', top: 20, right: 20, zIndex: 1000 }}>
      <label style={{ background: '#fff', padding: '8px 12px', borderRadius: 4, cursor: 'pointer' }}>
        Upload Image
        <input type="file" accept="image/*" onChange={handleFileChange} style={{ display: 'none' }}/>
      </label>
    </div>
  );
}
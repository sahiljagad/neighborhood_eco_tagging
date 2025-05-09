import { useEffect, useState } from 'react';
import MapView from './components/MapView';
import UploadButton from './components/UploadButton';
import { type Sighting } from './types';


function App() {

  const [sightings, setSightings] = useState<Sighting[]>([]);

  useEffect(() => {
    // Fetch sightings from the backend
    fetch('http://localhost:8000/sightings/')
      .then(res => res.json())
      .then((data: Sighting[]) => {
        setSightings(data);
        console.log('Fetched sightings:', data);
      })
      .catch(err => console.error('Error fetching sightings:', err));
  }, []);

  const handleImageUpload = (file: File, location: [number, number] | null) => {
    console.log('Image:', file);
    console.log('Location:', location);
    if (!file || !location) return;
  
    const formData = new FormData();
    formData.append('file', file);

    const [latitude, longitude] = location;
    const url = `http://localhost:8000/upload/?latitude=${latitude}&longitude=${longitude}`;

    fetch(url, {
      method: 'POST',
      body: formData,
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error('Upload failed');
        }
        return res.json();
      })
      .then((data) => {
        console.log('Upload successful:', data);
        setSightings([...sightings, data]);
      })
      .catch((err) => {
        console.error('Error uploading image:', err);
      });
  };

  return (
    <div>
      <UploadButton onImageUpload={handleImageUpload}/>
      <MapView sightings={sightings}/>
    </div>
  );
}

export default App;

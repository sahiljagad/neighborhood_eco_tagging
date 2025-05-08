import { useState } from 'react';
import MapView from './components/MapView';
import UploadButton from './components/UploadButton';


function App() {

  const [markerLocations, setMarkerLocations] = useState<[number, number][]>([]);
  console.log(markerLocations);

  const handleImageUpload = (file: File, location: [number, number] | null) => {
    console.log('Image:', file);
    console.log('Location:', location);
    if (!file || !location) return;
    if (location) {
      setMarkerLocations([...markerLocations, location]);
    }
    // need to pass in data for map locations
    // TODO: send the file and location to the backend DB
  };

  return (
    <div>
      <UploadButton onImageUpload={handleImageUpload}/>
      <MapView markerLocations={markerLocations}/>
    </div>
  );
}

export default App;

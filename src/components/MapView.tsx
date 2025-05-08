import { MapContainer, Marker, TileLayer } from 'react-leaflet'
import './MapView.css';

interface MapViewProps {
    markerLocations: [number, number][];
}

export default function MapView({markerLocations}: MapViewProps) {
    return (
        <div className='map-container'>
            <MapContainer center={[37.572676, -121.999605]} zoom={15} scrollWheelZoom={false}
                style={{ height: '70vh', width: '80vw',
                    borderRadius: '10px', 
                    boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
                }}>
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                { 
                    markerLocations.map((location, index) => <Marker key={index} position={[...location]} />)
                }
                
            </MapContainer>
        </div>
    );
}
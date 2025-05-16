import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet'
import './MapView.css';
import type { Sighting } from '../types';
import type { LatLngExpression } from 'leaflet';

interface MapViewProps {
    sightings: Sighting[];
}

const JITTER_RADIUS = 0.0001; // This defines how far the jitter can go from the original point

const applyJitter = (latitude: number, longitude: number) => {
    // Apply random jitter to latitude and longitude
    const jitterLat = latitude + (Math.random() - 0.5) * 2 * JITTER_RADIUS;
    const jitterLon = longitude + (Math.random() - 0.5) * 2 * JITTER_RADIUS;

    return [jitterLat, jitterLon];
};

export default function MapView({sightings}: MapViewProps) {
    return (
        <div className='map-container'>
            <MapContainer center={[37.572676, -121.999605]} zoom={15} maxZoom={25} // allow deep zoomscrollWheelZoom
                style={{ height: '70vh', width: '80vw',
                    borderRadius: '10px', 
                    boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
                }}>
                <TileLayer 
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    minZoom={3}
                    maxZoom={25}
                />
                { 
                    sightings.map((sighting, index) => 
                        <Marker key={index} position={applyJitter(sighting.latitude, sighting.longitude) as LatLngExpression} >
                            <Popup>
                                <div className='popup-content'>
                                    <h3>{sighting.species}</h3>
                                    <p>{new Date(sighting.timestamp).toLocaleString('en-US', {timeZone: 'America/Los_Angeles'})}</p>
                                    <img src={`../uploads/${sighting.filename}`} alt={sighting.species} height={60} width={60}/>
                                </div>
                            </Popup>
                        </Marker>
                )
                }
                
            </MapContainer>
        </div>
    );
}
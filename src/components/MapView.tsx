import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet'
import './MapView.css';
import type { Sighting } from '../types';

interface MapViewProps {
    sightings: Sighting[];
}

export default function MapView({sightings}: MapViewProps) {
    return (
        <div className='map-container'>
            <MapContainer center={[37.572676, -121.999605]} zoom={15} scrollWheelZoom
                style={{ height: '70vh', width: '80vw',
                    borderRadius: '10px', 
                    boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
                }}>
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                { 
                    sightings.map((sighting, index) => 
                        <Marker key={index} position={[sighting.latitude, sighting.longitude]} >
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
import {
  MapContainer,
  TileLayer,
  Marker,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function MapView({
  depot,
  collectionPoints,
}) {
  const center = [50.9271, 11.5892];

  return (
    <MapContainer
      center={center}
      zoom={13}
      style={{ height: "100vh", width: "100%" }}
    >
      <TileLayer url="https://tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {/* DEPOT */}
      {depot && (
        <Marker position={[depot.lat, depot.lng]} />
      )}

      {/* POINTS */}
      {collectionPoints.map((p, i) => (
        <Marker
          key={i}
          position={[p.lat, p.lng]}
        />
      ))}
    </MapContainer>
  );
}
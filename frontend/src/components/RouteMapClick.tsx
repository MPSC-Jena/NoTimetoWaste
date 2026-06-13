import { useMapEvents } from "react-leaflet";

export default function RouteMapClick() {
  useMapEvents({
    click(e) {
      console.log(e.latlng);
    },
  });

  return null;
}
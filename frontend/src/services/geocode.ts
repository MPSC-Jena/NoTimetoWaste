import axios from "axios";

export async function geocode(address: string) {
  const res = await axios.get(
    "https://nominatim.openstreetmap.org/search",
    {
      params: {
        format: "json",
        q: address,
      },
    }
  );

  const data = res.data?.[0];

  if (!data) return null;

  return {
    lat: parseFloat(data.lat),
    lng: parseFloat(data.lon),
  };
}
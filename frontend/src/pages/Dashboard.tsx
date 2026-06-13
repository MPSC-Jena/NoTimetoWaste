import { useState } from "react";
import { Box } from "@mui/material";

import MapView from "../components/MapView";
import ControlPanel from "../components/ControlPanel";

import type { Point } from "../types/point";
import type { Truck } from "../types/truck";

export default function Dashboard() {
  const [depot, setDepot] = useState<Point | null>(null);
  const [collectionPoints, setCollectionPoints] = useState<Point[]>([]);
  const [truck, setTruck] = useState<Truck>({
    width: 2.5,
    length: 10,
    turningRadius: 12,
    height: 3,
  });

  return (
    <Box sx={{ display: "flex", height: "100vh" }}>
      <Box sx={{ width: 350, p: 2 }}>
        <ControlPanel
          depot={depot}
          setDepot={setDepot}
          collectionPoints={collectionPoints}
          setCollectionPoints={setCollectionPoints}
        />
      </Box>

      <Box sx={{ flex: 1 }}>
        <MapView
          depot={depot}
          collectionPoints={collectionPoints}
        />
      </Box>
    </Box>
  );
}
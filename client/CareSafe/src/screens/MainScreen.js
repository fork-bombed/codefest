import React, { useState } from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { MapContainer, TileLayer } from 'react-leaflet';
import { SwipeablePanel } from 'rn-swipeable-panel';

const MainScreen = () => {
    const centerPosition = [51.505, -0.09]; // Sample latitude and longitude. You can replace with your preferred coordinates

    // useEffect(() => {
    //     document.body.style.overflow = "hidden";
     
    //     return () => {
    //        document.body.style.overflow = "auto";
    //     }
    //  }, []);

    const [panelProps, setPanelProps] = useState({
        fullWidth: true,
        openLarge: true,
        showCloseButton: true,
        style: {overflow: 'hidden'},
        closeOnTouchOutside: true,
        allowTouchOutside: true,
        showCloseButton: false,
        onClose: () => closePanel(),
        onPressCloseButton: () => closePanel(),
        // ...or any prop you want
      });
      const [isPanelActive, setIsPanelActive] = useState(true);
    
      const openPanel = () => {
        setIsPanelActive(true);
      };
    
      const closePanel = () => {
        setIsPanelActive(true);
      };

  return (
    <View style={{flex: 1, overflow: 'hidden'}}>
        <SwipeablePanel {...panelProps} isActive={isPanelActive}>
            <View style={{ height: 40, backgroundColor: 'white', alignItems: 'center', justifyContent: 'center' }}>
            <Text>Swipe Up Panel Content</Text>
            </View>
        </SwipeablePanel>
    <View style={{flex: 1}}>
  <MapContainer center={centerPosition} zoom={13} style={{ width: '100vw', height: '100vh' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
    </MapContainer>
    </View>
    </View>
    
    
  );

    const styles = StyleSheet.create({
      container: {
        flex: 1,
      },
      map: {
        ...StyleSheet.absoluteFillObject,
      },
    });
}

export default MainScreen;

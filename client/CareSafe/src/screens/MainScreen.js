import React from 'react';
import { StyleSheet, View, Animated, Dimensions } from 'react-native';
import { WebView } from 'react-native-webview';
import { PanGestureHandler, State } from 'react-native-gesture-handler';
import AppointmentScreen from './AppointmentScreen';

const MainScreen = ({ navigation }) => {
  const htmlContent = `
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
        <style>
            body { padding: 0; margin: 0; }
            html, body, #map { height: 100%; width: 100%; }
        </style>
    </head>
    <body>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        var map = L.map('map', {
            center: [51.505, -0.09],
            zoom: 13,
            zoomControl: false  // This disables the zoom control
        });
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: ''
        }).addTo(map);
    </script>
    </body>
    </html>
  `;

  const maxPanelHeight = Dimensions.get('window').height - 50; // Consider some offset for usability
  const minPanelHeight = 300;
  const translateY = new Animated.Value(0);
  const panelHeight = new Animated.Value(minPanelHeight);

  const onGestureEvent = Animated.event(
    [{ nativeEvent: { translationY: translateY } }],
    { useNativeDriver: false }
  );

  const onHandlerStateChange = event => {
    if (event.nativeEvent.oldState === State.ACTIVE) {
      const dragDirection = event.nativeEvent.velocityY; // Determines drag direction
      const draggedDistance = event.nativeEvent.translationY;

      if (dragDirection <= 0 && Math.abs(draggedDistance) > 40) {
        // Dragged upwards
        Animated.timing(panelHeight, {
          toValue: maxPanelHeight,
          duration: 300,
          useNativeDriver: false,
        }).start();
      } else if (dragDirection > 0 && Math.abs(draggedDistance) > 40) {
        // Dragged downwards
        Animated.timing(panelHeight, {
          toValue: minPanelHeight,
          duration: 300,
          useNativeDriver: false,
        }).start();
      } else {
        // If dragged distance is less than threshold, reset panel's height
        Animated.timing(panelHeight, {
          toValue: minPanelHeight,
          duration: 300,
          useNativeDriver: false,
        }).start();
      }

      translateY.setValue(0); // Reset the translation value
    }
  };

  return (
    <View style={styles.container}>
      <WebView 
        source={{ html: htmlContent }}
        style={styles.webView}
        scalesPageToFit={true}
      />
      
      <PanGestureHandler
        onGestureEvent={onGestureEvent}
        onHandlerStateChange={onHandlerStateChange}
      >
        <Animated.View
          style={[
            styles.panel,
            {
              height: panelHeight,
              transform: [{ translateY: translateY }],
            },
          ]}
        >
          <View style={styles.panelContent}>
            <View style={styles.panelHandle} />
          </View>
          <AppointmentScreen navigation={navigation} />
        </Animated.View>
      </PanGestureHandler>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  webView: {
    flex: 1,
  },
  panel: {
    position: 'absolute',
    height: 300,
    width: '100%',
    bottom: 0,
    backgroundColor: 'white',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
  },
  panelContent: {
    padding: 20,
    alignItems: 'center',
  },
  panelHandle: {
    width: 40,
    height: 6,
    backgroundColor: '#ccc',
    borderRadius: 3,
  },
});

export default MainScreen;
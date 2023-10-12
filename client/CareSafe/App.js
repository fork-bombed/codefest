import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import LoginScreen from './src/screens/LoginScreen';
import MainScreen from './src/screens/MainScreen';
import AppointmentScreen from './src/screens/AppointmentScreen';


const Stack = createStackNavigator();

// useEffect(() => {
//   // Applying on mount
//           document.body.style.overflow = "hidden";
//   // Applying on unmount    
//           return () => {
//             document.body.style.overflow = "visible";
//           }
//         }, [])

const App = () => {
  return (
    <NavigationContainer style={{flex: 1, overflow: 'hidden'}}>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Main" component={MainScreen} />
        <Stack.Screen name="Appointments" component={AppointmentScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    overflow: 'hidden',
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

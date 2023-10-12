import { StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import LoginScreen from './src/screens/LoginScreen';
import MainScreen from './src/screens/MainScreen';
import 'react-native-gesture-handler';
import CurrentAppointmentScreen from './src/screens/CurrentAppointmentScreen';
import AppointmentScreen from './src/screens/AppointmentScreen';


const Stack = createStackNavigator();

const App = () => {
  return (
    <NavigationContainer style={{flex: 1, overflow: 'hidden'}}>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Main" component={MainScreen} />
        <Stack.Screen name="Appointment" component={CurrentAppointmentScreen} />
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

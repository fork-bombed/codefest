// LoginScreen.js

import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  Image,
  Button,
  TouchableOpacity
} from 'react-native';

export default function LoginScreen({ navigation }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const response = await fetch('http://localhost:5000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password })
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      const { token } = await response.json();
      // Save the token to local storage
      localStorage.setItem('token', token);
      console.log('Login successful. Token:', token);
      // Navigate to the main app screen
      navigation.navigate('Main');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <View style={styles.container}>

      <Image source={require('../../assets/CareSafe.png')} style={styles.logo} />

      <Text style={styles.title}>Welcome Back!</Text>

      <TextInput
        value={username}
        onChangeText={setUsername}
        placeholder="Username"
        style={styles.input}
      />

      <TextInput
        value={password}
        onChangeText={setPassword}
        placeholder="Password"
        secureTextEntry
        style={styles.input}
      />

      <TouchableOpacity onPress={handleLogin} style={styles.loginButton}>
        <Text style={styles.loginButtonText}>Login</Text>
      </TouchableOpacity>
    <Button title="Login" onPress={() => navigation.navigate('Main')} />
    </View>
  );
};



const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'white',
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 24,
    marginBottom: 20,
    color: '#333',
    fontWeight: 'bold',
  },
  input: {
    width: '100%',
    padding: 15,
    marginBottom: 10,
    backgroundColor: 'white',
    borderRadius: 5,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  loginButton: {
    width: '100%',
    padding: 15,
    backgroundColor: '#007BFF',
    borderRadius: 5,
    alignItems: 'center',
    justifyContent: 'center',
  },
  loginButtonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
  logo: {
    width: 350,
    height: 350,
    marginBottom: 20,
    resizeMode: 'contain',
  },
});

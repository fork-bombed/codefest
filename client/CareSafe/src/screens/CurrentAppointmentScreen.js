import React, { useState, useRef, useEffect } from 'react';
import { View, Text, StyleSheet, Alert, Animated, PanResponder } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import '@react-navigation/native';

const CurrentAppointmentScreen = () => {
    const [currentAppointment, setCurrentAppointment] = useState(null);

    const [isCheckedIn, setCheckedIn] = useState(false);
    const translateX = useRef(new Animated.Value(0)).current;
    const panResponder = PanResponder.create({
        onStartShouldSetPanResponder: () => true,
        onPanResponderMove: Animated.event([null, { dx: translateX }], { useNativeDriver: false }),
        onPanResponderRelease: () => {
        if (isCheckedIn) {
            // If already checked in, allow checkout by sliding left
            if (translateX.__getValue() <= -150) {
            setCheckedIn(false);
            Animated.timing(translateX, {
                toValue: 0,
                duration: 300,
                useNativeDriver: false,
            }).start();
            } else {
            Animated.spring(translateX, {
                toValue: 0,
                useNativeDriver: false,
            }).start();
            }
        } else {
            // If checked out, allow check-in by sliding right
            if (translateX.__getValue() >= 150) {
            setCheckedIn(true);
            Animated.timing(translateX, {
                toValue: 0,
                duration: 300,
                useNativeDriver: false,
            }).start();
            } else {
            Animated.spring(translateX, {
                toValue: 0,
                useNativeDriver: false,
            }).start();
            }
        }
        },
    });

    const onCheckIn = async () => {
        try {
            const token = await AsyncStorage.getItem('token');
            const response = await fetch(`https://caresafe.azurewebsites.net/user/appointment/${currentAppointment.id}/checkin`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });
    
            if (!response.ok) {
                throw new Error('Failed to check-in');
            }
    
            // Successfully checked in
            setCheckedIn(true);
        } catch (error) {
            console.error(error);
            Alert.alert("Error", "Failed to check-in.");
        }
    };
    

    const [showSlider, setShowSlider] = useState(true); // State to control visibility of the slider.

    // Modify this part of the panResponder to hide the slider after checking in:
    onPanResponderRelease: () => {
        if (isCheckedIn) {
            // Allow checkout by sliding left
            if (translateX.__getValue() <= -150) {
                setCheckedIn(false); 
                Animated.timing(translateX, {
                    toValue: 0,
                    duration: 300,
                    useNativeDriver: false,
                }).start();
            } else {
                Animated.spring(translateX, {
                    toValue: 0,
                    useNativeDriver: false,
                }).start();
            }
        } else {
            // Allow check-in by sliding right
            if (translateX.__getValue() >= 150) {
                onCheckIn(); // Call the onCheckIn function here
                Animated.timing(translateX, {
                    toValue: 0,
                    duration: 300,
                    useNativeDriver: false,
                }).start();
            } else {
                Animated.spring(translateX, {
                    toValue: 0,
                    useNativeDriver: false,
                }).start();
            }
        }
    }
    

    useEffect(() => {
        const loadUserData = async () => {
            try {
                const token = await AsyncStorage.getItem('token');
                const response = await fetch('https://caresafe.azurewebsites.net/user', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });
    
                if (!response.ok) {
                    throw new Error('Failed to fetch user data');
                }
    
                const data = await response.json();
                setCheckedIn(data.checked_in); // Use the checked_in boolean to update our local state.
            } catch (error) {
                console.error(error);
                Alert.alert("Error", "Failed to fetch user data.");
            }
        };
    
        loadUserData();
    }, []);
    

    useEffect(() => {
        if (isCheckedIn) {
            setShowSlider(false);
        } else {
            setShowSlider(true);
        }
    }, [isCheckedIn]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const token = await AsyncStorage.getItem('token');
                if (token) {
                    const response = await fetch('https://caresafe.azurewebsites.net/user/appointments', {
                        method: 'GET',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json',
                        }
                    });

                    if (!response.ok) {
                        throw new Error('Failed to fetch appointments');
                    }

                    const data = await response.json();
                    const now = new Date();

                    const ongoingAppointment = data.appointments.find(app => {
                        const appointmentStart = new Date(app.date);
                        const appointmentEnd = new Date(app.date);
                        appointmentEnd.setMinutes(appointmentEnd.getMinutes() + app.duration);
                        return appointmentStart <= now && now <= appointmentEnd;
                    });

                    setCurrentAppointment(ongoingAppointment);
                }
            } catch (error) {
                console.error(error);
                Alert.alert("Error", "Failed to fetch current appointment.");
            }
        };

        fetchData();
    }, []);

    if (!currentAppointment) return <Text>No current appointment.</Text>;

    return (
        <View style={styles.container}>
            <View style={styles.card}>
                <Text style={styles.dateAndTime}>
                    {new Date(currentAppointment.date).toLocaleDateString()} - 
                    {new Date(currentAppointment.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </Text>
                <Text style={styles.clientName}>
                    {currentAppointment.client.first_name} {currentAppointment.client.last_name}
                </Text>
                <Text style={styles.address}>
                    {currentAppointment.client.address}
                </Text>
                <Text style={styles.address}>
                    {currentAppointment.duration} mins
                </Text>
            </View>
            {showSlider ? (
                <View style={styles.sliderContainer}>
                    <Animated.View {...panResponder.panHandlers} style={[styles.sliderButton, { transform: [{ translateX }] }]}>
                        <Text style={styles.sliderText}>{isCheckedIn ? 'Check Out' : 'Check In'}</Text>
                    </Animated.View>
                </View>
            ) : (
                <View style={styles.checkedInBox}>
                    <Text style={styles.checkedInText}>Checked In</Text>
                </View>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 10,
        backgroundColor: '#ffffff',
    },
    card: {
        backgroundColor: '#f4f4f4',
        padding: 20,
        marginBottom: 20,
        borderRadius: 8,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 5,
    },
    dateAndTime: {
        fontSize: 18,
        fontWeight: 'bold',
    },
    clientName: {
        fontSize: 16,
        marginTop: 10,
        color: '#444',
    },
    address: {
        fontSize: 14,
        marginTop: 5,
        color: '#777',
    },
    sliderContainer: {
        marginTop: 20,
        width: '100%',
        height: 60,
        borderColor: '#777',
        borderWidth: 1,
        borderRadius: 30,
        justifyContent: 'center',
        backgroundColor: '#ddd',
        overflow: 'hidden',  // This will ensure the button doesn't move outside the container.
    },
    sliderButton: {
        width: 125,
        height: 55,
        borderRadius: 30,  // Half of height to get a circular shape.
        backgroundColor: 'green',
        justifyContent: 'center',
        alignItems: 'center',
        marginTop: 5,
        marginBottom: 5,
        marginLeft: 2
    },
    sliderText: {
        color: '#fff',
        fontWeight: 'bold',
    },
    checkedInBox: {
        marginTop: 20,
        padding: 15,
        backgroundColor: 'green',
        borderRadius: 10,
        justifyContent: 'center',
        alignItems: 'center',
    },
    checkedInText: {
        color: 'white',
        fontSize: 18,
        fontWeight: 'bold',
    },
});

export default CurrentAppointmentScreen;

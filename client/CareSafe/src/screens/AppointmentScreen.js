import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, Alert, Animated, Easing, TouchableWithoutFeedback } from 'react-native';
import { ScrollView } from 'react-native-gesture-handler';  // <-- Import from react-native-gesture-handler
import AsyncStorage from '@react-native-async-storage/async-storage';

const AppointmentScreen = ({ navigation }) => {
    const [appointments, setAppointments] = useState([]);

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

                    const filteredAndSorted = data.appointments
                        .filter(app => {
                            const appointmentStart = new Date(app.date);
                            const appointmentEnd = new Date(app.date);
                            appointmentEnd.setMinutes(appointmentEnd.getMinutes() + app.duration);
                            return appointmentStart <= now && now <= appointmentEnd || now <= appointmentStart;
                        })  
                        .sort((a, b) => new Date(a.date) - new Date(b.date));  // Sort by date

                    setAppointments(filteredAndSorted);
                }
            } catch (error) {
                console.error(error);
                Alert.alert("Error", "Failed to fetch appointments.");
            }
        };

        fetchData();
    }, []);

    const pulseAnimation = useRef(new Animated.Value(0)).current;

    useEffect(() => {
        Animated.loop(
            Animated.sequence([
                Animated.timing(pulseAnimation, {
                    toValue: 1,
                    duration: 1000,
                    easing: Easing.sin,
                    useNativeDriver: true
                }),
                Animated.timing(pulseAnimation, {
                    toValue: 0,
                    duration: 1000,
                    easing: Easing.sin,
                    useNativeDriver: true
                })
            ])
        ).start();
    }, []);

    // Interpolate background color or border color
    const cardBackgroundColor = pulseAnimation.interpolate({
        inputRange: [0, 1],
        outputRange: ['#ffe6cc', '#ffd9b3'] // You can adjust these colors as needed
    });

    const isCurrentAppointment = (appointment) => {
        const now = new Date();
        const appointmentStart = new Date(appointment.date);
        const appointmentEnd = new Date(appointment.date);
        appointmentEnd.setMinutes(appointmentEnd.getMinutes() + appointment.duration);
        return now >= appointmentStart && now <= appointmentEnd;
    };

    const handleAppointmentClick = () => {
        navigation.navigate('Appointment');
    };

    return (
        <ScrollView style={styles.container}>
            {appointments.map((appointment, index) => (
                <Animated.View
                    key={appointment.id}
                    style={[
                        styles.card,
                        index === 0 ? (isCurrentAppointment(appointment) ? 
                            [styles.currentAppointmentCard, { backgroundColor: cardBackgroundColor }] :
                            styles.firstCard) : {}
                    ]}
                >
                    {index === 0 ? (
                        <>
                            <TouchableWithoutFeedback onPress={handleAppointmentClick}>
                                <View style={styles.topCardLayout}>
                                    <View>
                                        <Text style={isCurrentAppointment(appointment) ? styles.currentAppointmentText : styles.nextAppointmentText}>
                                            {isCurrentAppointment(appointment) ? "Current Appointment" : "Next Appointment"}
                                        </Text>
                                        <Text style={styles.nextAppointmentTime}>
                                            {new Date(appointment.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </Text>
                                    </View>
                                    <View style={styles.rightAlign}>
                                        <Text style={styles.clientName}>
                                            {appointment.client.first_name} {appointment.client.last_name}
                                        </Text>
                                        <Text style={styles.address}>
                                            {appointment.client.address}
                                        </Text>
                                    </View>
                                </View>
                            </TouchableWithoutFeedback>
                        </>
                    ) : (
                        <>
                            <Text style={styles.dateAndTime}>
                                {new Date(appointment.date).toLocaleDateString()} - 
                                {new Date(appointment.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </Text>
                            <Text style={styles.clientName}>
                                {appointment.client.first_name} {appointment.client.last_name}
                            </Text>
                            <Text style={styles.address}>
                                {appointment.client.address}
                            </Text>
                            <Text style={styles.address}>
                                {appointment.duration} mins
                            </Text>
                        </>
                    )}
                </Animated.View>
            ))}
        </ScrollView>
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
    firstCard: {
        shadowOpacity: 1,
        backgroundColor: '#e6ffe6',  // Slight green tint
        borderColor: '#e6ffe6',
    },
    currentAppointmentCard: {
        shadowOpacity: 1,
        backgroundColor: '#ffe6cc',  // Slight orange tint
        borderColor: '#ffe6cc',
    },
    rightAlign: {
        alignItems: 'flex-end',
        marginLeft: -10,
        marginTop: -15,
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
    nextAppointmentText: {
        fontSize: 14,
    },
    currentAppointmentText: {
        fontSize: 14,
    },
    topCardLayout: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        flex: 1,
    },
    nextAppointmentTime: {
        fontSize: 24,
        fontWeight: 'bold',
    },
});

export default AppointmentScreen;

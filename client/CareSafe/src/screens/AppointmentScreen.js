import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const AppointmentsScreen = () => {
    const [appointments, setAppointments] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const token = await AsyncStorage.getItem('token');
                if (token) {
                    const response = await fetch('http://localhost:5000/user/appointments', {
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
                    const filteredAndSorted = data.appointments
                        .filter(app => new Date(app.date) >= new Date())  // Only future appointments
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

    return (
        <ScrollView style={styles.container}>
            {appointments.map((appointment, index) => (
                <View 
                    key={appointment.id} 
                    style={[
                        styles.card, 
                        index === 0 
                            ? styles.firstCard 
                            : {}
                    ]}
                >
                    {index === 0 && new Date(appointment.date).toDateString() === new Date().toDateString() ? (
                        <View style={styles.topCardLayout}>
                            <View>
                                <Text style={styles.nextAppointmentText}>Next appointment</Text>
                                <Text style={styles.nextAppointmentTime}>
                                    {new Date(appointment.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </Text>
                            </View>
                            <View>
                                <Text style={styles.clientName}>
                                    {appointment.client.first_name} {appointment.client.last_name}
                                </Text>
                                <Text style={styles.address}>
                                    {appointment.client.address}
                                </Text>
                            </View>
                        </View>
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
                </View>
            ))}
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 10,
        backgroundColor: '#f4f4f4',
    },
    card: {
        backgroundColor: 'white',
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
        borderWidth: 0,
        backgroundColor: '#f4f4f4',
        borderColor: '#f4f4f4',
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
        fontSize: 20,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    nextAppointmentTime: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
    },
    topCardLayout: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        flex: 1,
    },
    nextAppointmentText: {
        fontSize: 16,
        fontWeight: 'bold',
        marginBottom: 5,
    },
    nextAppointmentTime: {
        fontSize: 20,
        fontWeight: 'bold',
    },
});

export default AppointmentsScreen;

import React, { useState, useEffect } from 'react';
import { View, TouchableOpacity, Text, StyleSheet, Image } from 'react-native';
import { Audio } from 'expo-av';
import * as FileSystem from 'expo-file-system';
import * as Network from 'expo-network';

export default function App() {
  const [status, setStatus] = useState('Ready');
  const [recording, setRecording] = useState(null);
  const [localIp, setLocalIp] = useState('');

  // Fetch the local IP address when the app is loaded
  useEffect(() => {
    const getLocalIp = async () => {
      const { ipAddress } = await Network.getIpAddressAsync();
      setLocalIp(ipAddress);
    };
    getLocalIp();
  }, []);

  const startRecording = async () => {
    try {
      const permission = await Audio.requestPermissionsAsync();
      if (permission.granted) {
        const { recording } = await Audio.Recording.createAsync(
          Audio.RecordingOptionsPresets.HIGH_QUALITY
        );
        setRecording(recording);
        setStatus('Recording...');
      } else {
        setStatus('Permission denied');
      }
    } catch (error) {
      console.error('Error starting recording', error);
      setStatus('Error starting recording');
    }
  };

  const stopRecording = async () => {
    try {
      if (recording) {
        await recording.stopAndUnloadAsync();
        const uri = recording.getURI();
        setRecording(null);
        setStatus('Uploading audio...');
        sendAudioToBackend(uri);
      }
    } catch (error) {
      console.error('Error stopping recording', error);
      setStatus('Error stopping recording');
    }
  };

  const toggleRecording = () => {
    if (recording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const sendAudioToBackend = async (uri) => {
    try {
      const audioFile = await FileSystem.readAsStringAsync(uri, {
        encoding: FileSystem.EncodingType.Base64,
      });

      // Use local IP for the backend URL
      const backendUrl = `http://${localIp}:5000/api/audio`;

      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ audio: audioFile }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const responseData = await response.json();
      console.log('Response data:', responseData);

      if (response.ok) {
        setStatus('Downloading audio response...');
        const blob = await response.blob();
        const localUri = `${FileSystem.cacheDirectory}response.wav`;
        const fileBase64 = await blob.text();
        await FileSystem.writeAsStringAsync(localUri, fileBase64, {
          encoding: FileSystem.EncodingType.Base64,
        });
        setStatus('Audio saved. Playing...');
        playReceivedAudio(localUri);
      } else {
        console.error('Failed to process audio:', responseData);
        setStatus('Error processing audio');
      }
    } catch (error) {
      console.error('Error uploading audio to backend', error);
      setStatus('Error uploading audio');
    }
  };

  const playReceivedAudio = async (uri) => {
    try {
      const { sound } = await Audio.Sound.createAsync({ uri });
      await sound.playAsync();
      setStatus('Playing received audio...');
    } catch (error) {
      console.error('Error playing received audio', error);
      setStatus('Error playing received audio');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.statusText}>{status}</Text>
      <TouchableOpacity style={styles.microphoneButton} onPress={toggleRecording}>
        <Image
          source={{ uri: 'https://cdn-icons-png.flaticon.com/512/786/786205.png' }}
          style={styles.microphoneIcon}
        />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  statusText: {
    fontSize: 18,
    marginBottom: 20,
    textAlign: 'center',
  },
  microphoneButton: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#f44336',
    justifyContent: 'center',
    alignItems: 'center',
  },
  microphoneIcon: {
    width: 50,
    height: 50,
  },
});

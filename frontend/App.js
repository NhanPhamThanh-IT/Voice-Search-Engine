import React, { useState } from 'react';
import { View, Button, Text, StyleSheet } from 'react-native';
import { Audio } from 'expo-av';
import * as FileSystem from 'expo-file-system';

export default function App() {
  const [recording, setRecording] = useState(null);
  const [status, setStatus] = useState('Ready to Record');
  const [isRecording, setIsRecording] = useState(false);

  const startRecording = async () => {
    try {
      const permission = await Audio.requestPermissionsAsync();
      if (permission.granted) {
        const { recording } = await Audio.Recording.createAsync(
          Audio.RecordingOptionsPresets.HIGH_QUALITY
        );
        setRecording(recording);
        setIsRecording(true);
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
        setIsRecording(false);
        setStatus('Recording stopped');
        const uri = recording.getURI();
        sendAudioToBackend(uri);
      }
    } catch (error) {
      console.error('Error stopping recording', error);
      setStatus('Error stopping recording');
    }
  };

  const sendAudioToBackend = async (uri) => {
    try {
      const audioFile = await FileSystem.readAsStringAsync(uri, {
        encoding: FileSystem.EncodingType.Base64,
      });
      const response = await fetch('http://10.0.2.2:5000/api/audio', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          audio: audioFile,
        }),
      });
      const responseData = await response.json();
      if (response.ok) {
        console.log('Audio file uploaded successfully');
      } else {
        console.error('Failed to upload audio file:', responseData);
      }
    } catch (error) {
      console.error('Error uploading audio to backend', error);
    }
  };

  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const playRecording = async () => {
    try {
      if (recording) {
        const { sound } = await recording.createNewLoadedSoundAsync();
        await sound.playAsync();
        setStatus('Playing Recording');
      } else {
        console.error('No recording available to play');
        setStatus('No recording available to play');
      }
    } catch (error) {
      console.error('Error playing recording', error);
      setStatus('Error playing recording');
    }
  };

  return (
    <View style={styles.container}>
      <Text>{status}</Text>
      <Button title={isRecording ? 'Stop Recording' : 'Start Recording'} onPress={toggleRecording} />
      {recording && !isRecording && <Button title="Play Recording" onPress={playRecording} />}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

// App.js
import React, { useState } from 'react';
import { View, TouchableOpacity, StyleSheet, Text } from 'react-native';
import { Audio } from 'expo-av';
import axios from 'axios';

export default function App() {
  const [recording, setRecording] = useState(null);
  const [playing, setPlaying] = useState(false);

  const startRecording = async () => {
    try {
      console.log('Requesting permissions...');
      const permission = await Audio.requestPermissionsAsync();

      if (permission.status === 'granted') {
        console.log('Starting recording...');
        await Audio.setAudioModeAsync({ allowsRecordingIOS: true });
        const { recording } = await Audio.Recording.createAsync(
          Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY
        );
        setRecording(recording);
        console.log('Recording started');
      } else {
        console.error('Permission to access microphone denied');
      }
    } catch (err) {
      console.error('Failed to start recording', err);
    }
  };

  const stopRecording = async () => {
    console.log('Stopping recording...');
    setRecording(null);
    await recording.stopAndUnloadAsync();
    const uri = recording.getURI();
    console.log('Recording stopped and stored at', uri);

    const formData = new FormData();
    formData.append('file', {
      uri,
      name: 'audio.wav',
      type: 'audio/wav',
    });

    try {
      console.log('Uploading audio to backend...');
      const response = await axios.post('http://192.168.2.152:5000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      console.log('Audio uploaded, playing response...');
      playAudio(response.data.audio_url);
    } catch (err) {
      console.error('Failed to upload audio', err);
    }
  };

  const playAudio = async (audioUrl) => {
    try {
      const { sound } = await Audio.Sound.createAsync({ uri: audioUrl });
      setPlaying(true);
      sound.setOnPlaybackStatusUpdate((status) => {
        if (!status.isPlaying) {
          setPlaying(false);
        }
      });
      await sound.playAsync();
    } catch (err) {
      console.error('Failed to play audio', err);
    }
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity
        style={[styles.microphoneButton, recording && styles.recording]}
        onPress={recording ? stopRecording : startRecording}
        accessibilityLabel={recording ? 'Dừng ghi âm' : 'Bắt đầu ghi âm'}
        accessibilityHint={recording ? 'Nhấn để dừng ghi âm' : 'Nhấn để bắt đầu ghi âm'}
        accessibilityRole="button"
      >
        <Text style={styles.buttonText}>{recording ? 'Dừng' : 'Ghi âm'}</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center',
    backgroundColor: '#FAFAFA',
  },
  microphoneButton: {
    width: 100,
    height: 100,
    backgroundColor: '#4CAF50',
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
  },
  recording: {
    backgroundColor: '#F44336',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 22,
    fontWeight: 'bold',
  },
});


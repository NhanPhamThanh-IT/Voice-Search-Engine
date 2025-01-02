import React, { useState } from 'react';
import { View, TouchableOpacity, StyleSheet, Text, ScrollView, Dimensions, Image } from 'react-native';
import { Audio } from 'expo-av';
import axios from 'axios';

export default function App() {
  const [recording, setRecording] = useState(null);
  const [playing, setPlaying] = useState(false);
  const [content, setContent] = useState('');

  const { width } = Dimensions.get('window');
  const dynamicMargin = width * 0.025;
  const dynamicPadding = width * 0.04;

  const startRecording = async () => {
    try {
      const permission = await Audio.requestPermissionsAsync();
      if (permission.status === 'granted') {
        await Audio.setAudioModeAsync({ allowsRecordingIOS: true });
        const { recording } = await Audio.Recording.createAsync(
          Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY
        );
        setRecording(recording);
      } else {
        console.error('Permission to access microphone denied');
      }
    } catch (err) {
      console.error('Failed to start recording', err);
    }
  };

  const stopRecording = async () => {
    setRecording(null);
    await recording.stopAndUnloadAsync();
    const uri = recording.getURI();

    const formData = new FormData();
    formData.append('file', {
      uri,
      name: 'audio.wav',
      type: 'audio/wav',
    });

    try {
      const response = await axios.post('http://192.168.2.152:5000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      const { content, audio_url } = response.data;
      setContent(content);
      playAudio(audio_url);
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
      {content && (
        <>
          <Image
            source={require('./assets/bot.png')}
            style={[styles.image]}
          />
          <ScrollView
            contentContainerStyle={[
              styles.contentContainer,
              { marginHorizontal: dynamicMargin, paddingHorizontal: dynamicPadding },
            ]}
          >
            <Text style={styles.contentText} accessibilityRole="text">
              {content}
            </Text>
          </ScrollView>
        </>
      )}
      <View style={styles.footer}>
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
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center',
    backgroundColor: '#FAFAFA',
    paddingTop: 40,
  },
  footer: {
    position: 'absolute',
    bottom: 20,
    width: '100%',
    justifyContent: 'center',
    alignItems: 'center',
  },
  microphoneButton: {
    width: 100,
    height: 100,
    backgroundColor: '#4CAF50',
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
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
  contentContainer: {
    marginTop: 10,
    paddingTop: 15,
    paddingBottom: 20,
    backgroundColor: '#fff',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  contentText: {
    fontSize: 16,
    color: '#333',
    lineHeight: 24,
    textAlign: 'justify',
  },
  image: {
    alignSelf: 'flex-end',
    marginRight: 10,
    marginTop: 10,
    width: 50,
    height: 50,
  },
});
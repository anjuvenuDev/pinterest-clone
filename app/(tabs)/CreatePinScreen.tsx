import { useState } from 'react';
import { Alert, Image, Pressable, ScrollView, StyleSheet, TextInput } from 'react-native';

import { Text, View } from '@/components/Themed';

export default function CreatePinScreen() {
  const [image, setImage] = useState(
    'https://notjustdev-dummy.s3.us-east-2.amazonaws.com/pinterest/0.jpeg'
  );
  const [title, setTitle] = useState('');

  const onSubmit = () => {
    if (!image || !title) {
      Alert.alert('Please enter image URL and title');
      return;
    }

    Alert.alert('Pin created');
    setTitle('');
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Image source={{ uri: image }} style={styles.image} />

      <Text style={styles.label}>Image URL</Text>
      <TextInput
        value={image}
        onChangeText={setImage}
        style={styles.input}
        placeholder="https://example.com/image.jpg"
      />

      <Text style={styles.label}>Title</Text>
      <TextInput
        value={title}
        onChangeText={setTitle}
        style={styles.input}
        placeholder="Type pin title"
      />

      <Pressable onPress={onSubmit} style={styles.button}>
        <Text style={styles.buttonText}>Create Pin</Text>
      </Pressable>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 10,
  },
  image: {
    width: '100%',
    aspectRatio: 1,
    borderRadius: 15,
    marginBottom: 12,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 6,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    marginBottom: 12,
    backgroundColor: 'white',
  },
  button: {
    backgroundColor: 'black',
    padding: 14,
    borderRadius: 24,
    alignItems: 'center',
    marginTop: 8,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
});

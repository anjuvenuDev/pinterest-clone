import { useState } from 'react';
import { Alert, Image, Pressable, ScrollView, StyleSheet, TextInput } from 'react-native';

import { Text, View } from '@/components/Themed';
import { ingestRecipe } from '@/services/api';

export default function CreatePinScreen() {
  const [image, setImage] = useState(
    'https://notjustdev-dummy.s3.us-east-2.amazonaws.com/pinterest/0.jpeg'
  );
  const [title, setTitle] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const onSubmit = async () => {
    if (!image || !title) {
      Alert.alert('Please enter image URL and title');
      return;
    }

    try {
      setSubmitting(true);
      const result = await ingestRecipe(image, title);
      Alert.alert('Recipe imported', result.message);
      setTitle('');
    } catch {
      Alert.alert('Import failed', 'Unable to reach backend. Check API URL and backend status.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Image source={{ uri: image }} style={styles.image} />

      <Text style={styles.label}>Image URL / Source URL</Text>
      <TextInput
        value={image}
        onChangeText={setImage}
        style={styles.input}
        placeholder="https://example.com/image.jpg"
        autoCapitalize="none"
      />

      <Text style={styles.label}>Creator Notes / Title</Text>
      <TextInput
        value={title}
        onChangeText={setTitle}
        style={styles.input}
        placeholder="Type recipe note or title"
      />

      <Pressable onPress={onSubmit} style={[styles.button, submitting && styles.buttonDisabled]} disabled={submitting}>
        <Text style={styles.buttonText}>{submitting ? 'Importing...' : 'Import Recipe'}</Text>
      </Pressable>

      <View style={styles.infoCard}>
        <Text style={styles.infoTitle}>Creator ingestion flow</Text>
        <Text style={styles.infoText}>This screen now calls the backend creator ingestion service and queues scraping/indexing jobs.</Text>
      </View>
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
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  infoCard: {
    marginTop: 18,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 10,
    padding: 12,
    backgroundColor: '#f8f8f8',
  },
  infoTitle: {
    fontWeight: '700',
    marginBottom: 6,
  },
  infoText: {
    color: '#555',
    lineHeight: 20,
  },
});

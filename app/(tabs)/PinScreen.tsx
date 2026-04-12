import { Image, Pressable, StyleSheet } from 'react-native';
import { useEffect, useMemo, useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import { Ionicons } from '@expo/vector-icons';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context';

import { Text, View } from '@/components/Themed';
import pins from '@/app/data/pins';

export default function PinScreen() {
  const { id } = useLocalSearchParams<{ id?: string }>();
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const [ratio, setRatio] = useState(1);

  const pin = useMemo(() => pins.find((item) => item.id === id) ?? pins[0], [id]);

  useEffect(() => {
    if (!pin?.image) return;
    Image.getSize(
      pin.image,
      (width, height) => {
        if (width > 0 && height > 0) {
          setRatio(width / height);
        }
      },
      () => setRatio(1)
    );
  }, [pin?.image]);

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar style="light" />
      <View style={styles.root}>
        <Image source={{ uri: pin.image }} style={[styles.image, { aspectRatio: ratio }]} />
        <Text style={styles.title}>{pin.title}</Text>
        <Pressable onPress={() => router.back()} style={[styles.backBtn, { top: insets.top + 20 }]}>
          <Ionicons name="chevron-back" size={35} color="white" />
        </Pressable>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    backgroundColor: 'black',
  },
  root: {
    height: '100%',
    backgroundColor: 'white',
    borderTopLeftRadius: 30,
    borderTopRightRadius: 30,
  },
  image: {
    width: '100%',
    borderTopLeftRadius: 30,
    borderTopRightRadius: 30,
  },
  title: {
    margin: 10,
    fontSize: 24,
    fontWeight: '600',
    textAlign: 'center',
    lineHeight: 35,
  },
  backBtn: {
    position: 'absolute',
    left: 21,
  },
});

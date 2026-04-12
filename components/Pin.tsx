import { Image, StyleSheet, Pressable } from 'react-native';
import { Text, View } from '@/components/Themed';
import FontAwesome from '@expo/vector-icons/FontAwesome';
import { useEffect, useState } from 'react';
import { useRouter } from 'expo-router';

type PinItem = {
  id: string;
  image: string;
  title: string;
};

type PinProps = {
  pin: PinItem;
};

export default function Pin({ pin }: PinProps) {
    const { id, image, title } = pin;

    const [ratio, setRatio] = useState(1);
    const router = useRouter();

    const onLike = () => {}; 

    useEffect(() => {
      if (!image) return;
      Image.getSize(
        image,
        (width, height) => {
          if (width > 0 && height > 0) {
            setRatio(width / height);
          }
        },
        () => {
          // Keep default ratio when remote image size cannot be fetched.
          setRatio(1);
        }
      );
    }, [image]);

    const goToPinPage = () => {
        router.push({ pathname: '/PinScreen', params: { id } });
    };

  return (
    <Pressable onPress={goToPinPage} style={styles.pin}>
      <View>
        <Image
        source={{
            uri:image,
        }}
        style={[styles.image, {aspectRatio: ratio}]}
      />
    
    <Pressable onPress={onLike} style={styles.heartButton}>
        <FontAwesome name="heart-o" size={16} color="black" />
    </Pressable>
      </View>
      

      <Text style={styles.title} numberOfLines={2}>{title}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  title: {
    fontSize: 16,
    lineHeight:22,
    fontWeight: '600',
    margin: 5,
    color:'#181818'
  },
  image: {
    width: '100%',
    borderRadius: 15,
  },
  pin: {
    width: '100%',
    padding:4,
  },
  heartButton: {
    backgroundColor: "#D3CFD4",
    position: 'absolute',
    bottom: 10,
    right: 10,
    padding:5,
    borderRadius:20,
  }
});

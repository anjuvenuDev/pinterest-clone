import { Image, StyleSheet, Pressable } from 'react-native';
import { Text, View } from '@/components/Themed';
import FontAwesome from '@expo/vector-icons/FontAwesome';
import { useEffect, useState } from 'react';

export default function Pin(props: any) {
    const {image, title} = props.pin;

    const [ratio, setRatio] = useState(1);

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

  return (
    <View style={styles.pin}>
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
      

      <Text style={styles.title}>{title}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    margin: 10,
  },
  image: {
    width: '100%',
    borderRadius: 25,
  },
  pin: {
    width: '100%',
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

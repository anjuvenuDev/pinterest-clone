import { Image, ScrollView, StyleSheet } from 'react-native';

import { Text, View } from '@/components/Themed';
import Pin from '@/components/Pin';
import pins from '@/app/data/pins';

export default function ProfileScreen() {
  return (
    <ScrollView>
      <View style={styles.root}>
        <Image
          source={{
            uri: 'https://notjustdev-dummy.s3.us-east-2.amazonaws.com/avatars/1.jpg',
          }}
          style={styles.profileImage}
        />
        <Text style={styles.name}>Anjana</Text>
        <Text style={styles.subTitle}>150 followers · 40 following</Text>
        <Text style={styles.bio}>Building apps with React Native</Text>
      </View>

      <View style={styles.pins}>
        <View style={styles.column}>
          {pins.filter((_, index) => index % 2 === 0).map((pin) => <Pin pin={pin} key={pin.id} />)}
        </View>
        <View style={styles.column}>
          {pins.filter((_, index) => index % 2 === 1).map((pin) => <Pin pin={pin} key={pin.id} />)}
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  root: {
    alignItems: 'center',
    padding: 10,
  },
  profileImage: {
    width: 120,
    height: 120,
    borderRadius: 60,
  },
  name: {
    marginTop: 10,
    fontSize: 28,
    fontWeight: '600',
  },
  subTitle: {
    color: 'gray',
    marginVertical: 5,
    fontWeight: '600',
    letterSpacing: 0.5,
  },
  bio: {
    fontWeight: '600',
    lineHeight: 20,
  },
  pins: {
    padding: 10,
    flexDirection: 'row',
  },
  column: {
    flex: 1,
  },
});

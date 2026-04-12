import { StyleSheet, Image, ScrollView } from 'react-native';

import EditScreenInfo from '@/components/EditScreenInfo';
import { Text, View } from '@/components/Themed';
import Pin from '../../components/Pin';
import pins from '../data/pins';

export default function HomeScreen() {
  return (
    <ScrollView>
      <View style={styles.container}>
        <View style={styles.column}>
          {pins.filter((_, index)=> index%2 === 0).map(pin => <Pin pin={pin} key={pin.id}/>)}
        </View>
        <View style={styles.column}>
          {pins.filter((_, index)=> index%2 === 1).map(pin => <Pin pin={pin} key={pin.id}/>)}
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 10,
    flexDirection: 'row'
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    margin: 10,
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
  image: {
    width: "100%",
    height: 200,
    borderRadius:25,
  },
  pin: {
    width: "100%"
  },
  column:{
    flex: 1,
  }
});

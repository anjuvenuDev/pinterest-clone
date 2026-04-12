import { StyleSheet, Image, ScrollView } from 'react-native';

import EditScreenInfo from '@/components/EditScreenInfo';
import { Text, View } from '@/components/Themed';
import Pin from '../../components/Pin';

export default function HomeScreen() {
  return (
    <ScrollView>
      <View style={styles.container}>
      <Pin 
        pin={{
          title:"title",
          image:"https://notjustdev-dummy.s3.us-east-2.amazonaws.com/pinterest/0.jpeg"
          }}  
      />
      <Pin 
      pin={{
          title:"title2",
          image:"https://notjustdev-dummy.s3.us-east-2.amazonaws.com/pinterest/1.jpeg"
      }}   
      />
    </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 10,
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
  }
});

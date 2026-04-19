import { useCallback, useEffect, useMemo, useState } from 'react';
import { Image, RefreshControl, ScrollView, StyleSheet } from 'react-native';

import { Text, View } from '@/components/Themed';
import Pin from '@/components/Pin';
import { fetchFeed, fetchMyProfile } from '@/services/api';
import type { PinItem, UserProfile } from '@/types/pin';
import localPins from '@/app/data/pins';

const fallbackProfile: UserProfile = {
  id: 'demo-user',
  name: 'Anjana',
  email: 'anjana@example.com',
  roles: ['home-cook'],
  onboarding_completed: false,
  bookmarks: 0,
  likes: 0,
};

export default function ProfileScreen() {
  const [profile, setProfile] = useState<UserProfile>(fallbackProfile);
  const [bookmarks, setBookmarks] = useState<PinItem[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  const [usingFallback, setUsingFallback] = useState(false);

  const loadProfile = useCallback(async () => {
    setRefreshing(true);
    try {
      const [profileData, bookmarkFeed] = await Promise.all([
        fetchMyProfile(),
        fetchFeed({ bookmarked: true, limit: 30 }),
      ]);
      setProfile(profileData);
      setBookmarks(bookmarkFeed.items);
      setUsingFallback(false);
    } catch {
      setProfile(fallbackProfile);
      setBookmarks(localPins.slice(0, 6));
      setUsingFallback(true);
    } finally {
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadProfile();
  }, [loadProfile]);

  const leftColumn = useMemo(() => bookmarks.filter((_, index) => index % 2 === 0), [bookmarks]);
  const rightColumn = useMemo(() => bookmarks.filter((_, index) => index % 2 === 1), [bookmarks]);

  return (
    <ScrollView refreshControl={<RefreshControl refreshing={refreshing} onRefresh={loadProfile} />}>
      <View style={styles.root}>
        <Image
          source={{
            uri: 'https://notjustdev-dummy.s3.us-east-2.amazonaws.com/avatars/1.jpg',
          }}
          style={styles.profileImage}
        />
        <Text style={styles.name}>{profile.name}</Text>
        <Text style={styles.subTitle}>{`${profile.bookmarks} bookmarks · ${profile.likes} likes`}</Text>
        <Text style={styles.bio}>Roles: {profile.roles.join(', ') || 'home-cook'}</Text>
        {usingFallback ? <Text style={styles.meta}>Backend unavailable, showing local profile data</Text> : null}
      </View>

      <View style={styles.pins}>
        <View style={styles.column}>
          {leftColumn.map((pin) => <Pin pin={pin} key={pin.id} />)}
        </View>
        <View style={styles.column}>
          {rightColumn.map((pin) => <Pin pin={pin} key={pin.id} />)}
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
  meta: {
    color: '#666',
    fontWeight: '600',
    marginTop: 6,
  },
  pins: {
    padding: 10,
    flexDirection: 'row',
  },
  column: {
    flex: 1,
  },
});

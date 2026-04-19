import { useCallback, useEffect, useMemo, useState } from 'react';
import { RefreshControl, ScrollView, StyleSheet } from 'react-native';

import { Text, View } from '@/components/Themed';
import Pin from '@/components/Pin';
import { fetchFeed } from '@/services/api';
import type { PinItem } from '@/types/pin';
import localPins from '@/app/data/pins';

export default function HomeScreen() {
  const [pins, setPins] = useState<PinItem[]>(localPins);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [usingFallback, setUsingFallback] = useState(false);

  const loadFeed = useCallback(async (isRefresh = false) => {
    if (isRefresh) setRefreshing(true);
    else setLoading(true);

    try {
      const response = await fetchFeed({ limit: 30 });
      setPins(response.items);
      setUsingFallback(false);
    } catch {
      setPins(localPins);
      setUsingFallback(true);
    } finally {
      if (isRefresh) setRefreshing(false);
      else setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadFeed();
  }, [loadFeed]);

  const leftColumn = useMemo(() => pins.filter((_, index) => index % 2 === 0), [pins]);
  const rightColumn = useMemo(() => pins.filter((_, index) => index % 2 === 1), [pins]);

  return (
    <ScrollView
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={() => loadFeed(true)} />}
    >
      {loading ? <Text style={styles.infoText}>Loading feed...</Text> : null}
      {usingFallback ? <Text style={styles.infoText}>Using local feed fallback</Text> : null}

      <View style={styles.container}>
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
  container: {
    padding: 10,
    flexDirection: 'row',
  },
  column: {
    flex: 1,
  },
  infoText: {
    marginHorizontal: 12,
    marginTop: 10,
    color: '#666',
    fontWeight: '600',
  },
});

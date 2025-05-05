package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/redis/go-redis/v9"
)

const (
	cleanupInterval = 1 * time.Hour
	keyPrefix       = "url:"
)

func main() {
	rdb := redis.NewClient(&redis.Options{
		Addr:     "redis:6379", // Matches compose service name
		Password: "",
		DB:       0,
	})

	for {
		cleanupExpiredURLs(rdb)
		time.Sleep(cleanupInterval)
	}
}

func cleanupExpiredURLs(rdb *redis.Client) {
	ctx := context.Background()
	keys, err := rdb.Keys(ctx, keyPrefix+"*").Result()
	if err != nil {
		log.Printf("Error fetching keys: %v", err)
		return
	}

	for _, key := range keys {
		if ttl, err := rdb.TTL(ctx, key).Result(); err == nil {
			if ttl < 0 { // -1 = no expiration, -2 = key doesn't exist
				rdb.Del(ctx, key)
				log.Printf("Cleaned up key: %s", key)
			}
		}
	}
	fmt.Printf("Cleanup completed at %s\n", time.Now().Format(time.RFC3339))
}

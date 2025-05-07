package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/redis/go-redis/v9"
)

const (
	cleanupInterval = 1 * time.Hour
	keyPrefix       = "url:"
)

func main() {
	// Get Redis password from environment
	redisHost := os.Getenv("REDIS_HOST")
	if redisHost == "" {
		redisHost = "localhost"
	}

	redisPassword := os.Getenv("REDIS_PASSWORD")
	log.Printf("Connecting to Redis at %s with password: %s", redisHost, redisPassword)

	// Connect to Redis with password
	client := redis.NewClient(&redis.Options{
		Addr:     redisHost + ":6379",
		Password: redisPassword, // Set password here
		DB:       0,
	})

	// Test the connection
	ctx := context.Background()
	_, err := client.Ping(ctx).Result()
	if err != nil {
		log.Fatalf("Failed to connect to Redis: %v", err)
	}
	log.Printf("Connected to Redis successfully")

	// Run the cleanup once immediately
	cleanupExpiredURLs(client)

	// Then set up a ticker to run periodically
	ticker := time.NewTicker(cleanupInterval)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			cleanupExpiredURLs(client)
		}
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

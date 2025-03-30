package config

import (
	"encoding/json"
	"fmt"
	"github.com/kelseyhightower/envconfig"
	"os"
)

type Config struct {
	Host string `json:"host" envconfig:"host"`
	Port string `json:"port" envconfig:"port"`
}

func getConfigsFromJSON() (*Config, error) {
	var filePath string
	if os.Getenv("config") == "" {
		pwd, err := os.Getwd()
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}
		filePath = pwd + "/config/config.json"
	} else {
		filePath = os.Getenv("config")
	}

	file, err := os.Open(filePath)

	if err != nil {
		return &Config{}, err
	}

	decoder := json.NewDecoder(file)
	var config Config
	err = decoder.Decode(&config)

	if err != nil {
		return &Config{}, err
	}

	return &config, err
}

func getConfigsFromENV() (*Config, error) {
	var cfg Config

	err := envconfig.Process("APP_CONFIG", &cfg)
	if err != nil {
		return nil, err
	}

	return &cfg, nil
}

func GetConfig() (*Config, error) {
	if os.Getenv("KUBERNETES_PORT") == "" {
		return getConfigsFromJSON()
	}
	return getConfigsFromENV()
}

package tilt

import (
	"errors"
	"fmt"
	"github.com/go-kit/kit/log/level"
	"github.com/spf13/viper"
	"os"
	"path/filepath"
	"strings"
)

type Config struct {
	ConfigFile     string
	ConfigData     *viper.Viper
	EnabledEmitter string
}

func ParseConfig(configFile string) Config {
	_viper := viper.New()

	// Set Some Defaults
	_viper.SetDefault("general.logging_level", "INFO")
	_viper.SetDefault("general.logfile", "/dev/stdout")
	_viper.SetDefault("general.gravity_offset", 0.0)
	_viper.SetDefault("general.temperature_offset", 0)

	if _, err := os.Stat(configFile); errors.Is(err, os.ErrNotExist) {
		level.Debug(Logger).Log(
			"config.ParseConfig",
			fmt.Sprintf("Config file %s does not exist. Using all default values.", configFile),
		)
		_viper.SetDefault("stdout.enabled", true)
	} else {
		level.Debug(Logger).Log("config.ParseConfig", fmt.Sprintf("Using config file: %s", configFile))
		_viper.SetConfigType(filepath.Ext(configFile)[1:])
		_viper.SetConfigName(filepath.Base(configFile))
		_viper.AddConfigPath(filepath.Dir(configFile))

		err := _viper.ReadInConfig()
		if err != nil { // Handle errors reading the config file
			panic(fmt.Errorf("fatal error config file: %w", err))
		}
	}
	level.Debug(Logger).Log("config.ParseConfig", fmt.Sprintf("Log Level: %s", _viper.Get("general.logging_level")))
	level.Debug(Logger).Log("config.ParseConfig", fmt.Sprintf("Log File: %s", _viper.Get("general.logfile")))
	level.Debug(Logger).Log("config.ParseConfig", fmt.Sprintf("Gravity Offset: %f", _viper.Get("general.gravity_offset")))
	level.Debug(Logger).Log("config.ParseConfig", fmt.Sprintf("Temperature Offset: %d", _viper.Get("general.temperature_offset")))

	enabledEmitter := ""
	for _, emitter := range _viper.AllKeys() {
		_emitterPair := strings.Split(emitter, ".")
		if _emitterPair[1] == "enabled" {
			enabledEmitter = _emitterPair[0]
			break
		}
	}

	if len(enabledEmitter) == 0 {
		level.Debug(Logger).Log("config.ParseConfig", "No enabled emitters in configuration. Using 'stdout'")
		enabledEmitter = "stdout"
	}

	return Config{
		ConfigFile:     configFile,
		ConfigData:     _viper,
		EnabledEmitter: enabledEmitter,
	}
}

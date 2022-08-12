package cli

import (
	"fmt"
	"github.com/akamensky/argparse"
	"os"
)

type Config struct {
	ConfigFile string
	Daemonize  bool
}

func ParseArgs() Config {
	parser := argparse.NewParser("tilty", "A pluggable system to receive and transmit bluetooth events from the Tilt Hydrometer")

	configFile := parser.String("c", "config", &argparse.Options{
		Required: true,
		Help:     "Configuration file location",
	})

	daemonize := parser.Flag("r", "keep-running", &argparse.Options{
		Required: false,
		Default:  false,
		Help:     "Keep running until SIGTERM",
	})

	if err := parser.Parse(os.Args); err != nil {
		fmt.Println(parser.Usage(err))
		os.Exit(1)
	}

	return Config{
		ConfigFile: *configFile,
		Daemonize:  *daemonize,
	}
}

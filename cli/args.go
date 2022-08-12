package cli

import (
	"fmt"
	"github.com/akamensky/argparse"
	"github.com/myoung34/tilty/tilt"
	"os"
)

func ParseArgs() tilt.Config {
	parser := argparse.NewParser("tilty", "A pluggable system to receive and transmit bluetooth events from the Tilt Hydrometer")

	configFile := parser.String("c", "config", &argparse.Options{
		Required: true,
		Help:     "Configuration file location",
	})

	if err := parser.Parse(os.Args); err != nil {
		fmt.Println(parser.Usage(err))
		os.Exit(1)
	}

	return tilt.ParseConfig(*configFile)
}

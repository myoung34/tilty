package main

import (
	"fmt"
	"github.com/go-kit/kit/log/level"
	"github.com/myoung34/tilty/cli"
	"github.com/myoung34/tilty/tilt"
	"github.com/paypal/gatt"
	"github.com/paypal/gatt/examples/option"
)

func main() {
	tilt.SetLogging()
	config := cli.ParseArgs()
	level.Debug(tilt.Logger).Log("main", fmt.Sprintf("Using config file: %s", config.ConfigFile))
	level.Debug(tilt.Logger).Log("main", fmt.Sprintf("Daemonize: %t", config.Daemonize))

	level.Info(tilt.Logger).Log("main", "Scanning...")
	device, err := gatt.NewDevice(option.DefaultClientOptions...)
	if err != nil {
		level.Error(tilt.Logger).Log("main", fmt.Sprintf("Failed to open device, err: %s\n", err))
		return
	}
	device.Handle(gatt.PeripheralDiscovered(tilt.OnPeripheralDiscovered))
	device.Init(tilt.OnStateChanged)
	select {}
}

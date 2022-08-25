package main

import (
	"encoding/binary"
	"encoding/hex"
	"errors"
	"fmt"
	"github.com/go-kit/log/level"
	"github.com/go-playground/validator/v10"
	"github.com/myoung34/gatt"
	"github.com/myoung34/gatt/examples/option"
	"github.com/myoung34/tilty/cli"
	"github.com/myoung34/tilty/emitters"
	"github.com/myoung34/tilty/tilt"
	"reflect"
	"strings"
	"time"
)

var config = tilt.Config{}
var validate = validator.New()

var EmittersMap = map[string]interface{}{
	"webhook.emit": emitters.WebhookEmit,
	"sqlite.emit":  emitters.SQLiteEmit,
	"datadog.emit": emitters.DatadogEmit,
}

func main() {
	tilt.EnableLogging()
	config = cli.ParseArgs()
	tilt.SetLogging(fmt.Sprintf("%s", config.ConfigData.Get("general.logging_level")))

	level.Debug(tilt.Logger).Log("main", fmt.Sprintf("Using emitter: %s", config.EnabledEmitter))

	level.Info(tilt.Logger).Log("main", "Scanning...")
	device, err := gatt.NewDevice(option.DefaultClientOptions...)
	if err != nil {
		level.Error(tilt.Logger).Log("main", fmt.Sprintf("Failed to open device, err: %s\n", err))
		return
	}

	device.Handle(gatt.PeripheralDiscovered(OnPeripheralDiscovered))
	device.Init(OnStateChanged)
	select {}
}

func OnStateChanged(device gatt.Device, s gatt.State) {
	switch s {
	case gatt.StatePoweredOn:
		level.Info(tilt.Logger).Log("main.OnStateChanged", "Scanning...")
		device.Scan([]gatt.UUID{}, true)
		return
	default:
		device.StopScanning()
	}
}

func NewTilt(data []byte) (tilt.Payload, error) {
	// http://www.havlena.net/wp-content/themes/striking/includes/timthumb.php?src=/wp-content/uploads/ibeacon-packet.png&w=600&zc=1
	//pkt = b'   \x04>*                      \x02\x01x03\x01w\t  \xbc\xd0W\xef\x1e\x02\x01\x04\x1a\xffL\x00\x02\x15    \xa4\x95\xbb0\xc5\xb1KD\xb5\x12\x13p\xf0-t\xde  \x00B  \x03\xf7   \xc5\xa7'   # noqa
	//       |                  |           |                   |                                                    |                                                |      |         |          |  # noqa
	//       | preamble+header  |                         PDU                                                                                                                                     |  # noqa
	//       |     3 bytes      |                        x bytes (plen)                                                                                                                           |  # noqa
	//       |                  |           |    mac addr       |           uuid                                     |          unused data                           | major| minor   |   tx     |  # noqa
	//       |                  |           |                   |                                                    |
	if len(data) < 25 || binary.BigEndian.Uint32(data) != 0x4c000215 {
		return tilt.Payload{}, errors.New("not an iBeacon")
	}
	return tilt.Payload{
		ID:    strings.ToLower(strings.Replace(strings.ToUpper(hex.EncodeToString(data[4:8])+"-"+hex.EncodeToString(data[8:10])+"-"+hex.EncodeToString(data[10:12])+"-"+hex.EncodeToString(data[12:14])+"-"+hex.EncodeToString(data[14:20])), "-", "", -1)),
		Major: binary.BigEndian.Uint16(data[20:22]),
		Minor: binary.BigEndian.Uint16(data[22:24]),
	}, nil
}

func OnPeripheralDiscovered(p gatt.Peripheral, a *gatt.Advertisement, rssi int) {
	_tilt, err := NewTilt(a.ManufacturerData)
	if err == nil {
		payload := tilt.Payload{
			ID:        _tilt.ID,
			Mac:       p.ID(),
			Color:     tilt.TiltMap[_tilt.ID],
			Major:     _tilt.Major,
			Minor:     _tilt.Minor,
			Rssi:      rssi,
			Timestamp: time.Now().UTC().Unix(),
		}
		err = validate.Struct(payload)
		if err == nil {
			level.Info(tilt.Logger).Log("main.OnPeripheralDiscovered", fmt.Sprintf("%s [%s] temp: %d gravity: %d rssi: %d", payload.ID, payload.Color, payload.Major, payload.Minor, rssi))
			returnStr, _ := callEmitter(fmt.Sprintf("%s.emit", config.EnabledEmitter), payload, config.ConfigData.Get(config.EnabledEmitter))
			level.Info(tilt.Logger).Log("main.OnPeripheralDiscovered", returnStr)
		}

	}
}

func callEmitter(funcName string, payload tilt.Payload, emitterConfig interface{}) (result interface{}, err error) {
	level.Info(tilt.Logger).Log("main.callEmitter", fmt.Sprintf("Attempting to call %+v", funcName))
	_, ok := EmittersMap[funcName]
	if !ok {
		panic(fmt.Sprintf("Emitter '%s' not found'", strings.Split(funcName, ".")[0]))
	}
	f := reflect.ValueOf(EmittersMap[funcName])
	in := make([]reflect.Value, 2)
	in[0] = reflect.ValueOf(payload)
	in[1] = reflect.ValueOf(emitterConfig)
	var res = f.Call(in)
	result = res[0].Interface()
	return
}

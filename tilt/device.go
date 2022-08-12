package tilt

import (
	"encoding/binary"
	"encoding/hex"
	"errors"
	"fmt"
	"github.com/go-kit/kit/log/level"
	validator "github.com/go-playground/validator/v10"
	"github.com/paypal/gatt"
	"strings"
)

var validate = validator.New()

var TiltMap = map[string]string{
	"a495bb30c5b14b44b5121370f02d74de": "BLACK",
	"a495bb60c5b14b44b5121370f02d74de": "BLUE",
	"a495bb20c5b14b44b5121370f02d74de": "GREEN",
	"a495bb50c5b14b44b5121370f02d74de": "ORANGE",
	"a495bb80c5b14b44b5121370f02d74de": "PINK",
	"a495bb40c5b14b44b5121370f02d74de": "PURPLE",
	"a495bb10c5b14b44b5121370f02d74de": "RED",
	"a495bb70c5b14b44b5121370f02d74de": "YELLOW",
	"a495bb90c5b14b44b5121370f02d74de": "TEST",
	"25cc0b60914de76ead903f903bfd5e53": "MIGHTY",
}

type TiltPayload struct {
	Id    string
	Color string `validate:"required"`
	Major uint16
	Minor uint16
	Rssi  int
}

func OnStateChanged(device gatt.Device, s gatt.State) {
	switch s {
	case gatt.StatePoweredOn:
		level.Info(Logger).Log("main", "Scanning...")
		device.Scan([]gatt.UUID{}, true)
		return
	default:
		device.StopScanning()
	}
}

func NewTilt(data []byte) (TiltPayload, error) {
	if len(data) < 25 || binary.BigEndian.Uint32(data) != 0x4c000215 {
		return TiltPayload{}, errors.New("Not an iBeacon")
	}
	return TiltPayload{
		Id:    strings.ToLower(strings.Replace(strings.ToUpper(hex.EncodeToString(data[4:8])+"-"+hex.EncodeToString(data[8:10])+"-"+hex.EncodeToString(data[10:12])+"-"+hex.EncodeToString(data[12:14])+"-"+hex.EncodeToString(data[14:20])), "-", "", -1)),
		Major: binary.BigEndian.Uint16(data[20:22]),
		Minor: binary.BigEndian.Uint16(data[22:24]),
	}, nil
}

func OnPeripheralDiscovered(p gatt.Peripheral, a *gatt.Advertisement, rssi int) {
	b, err := NewTilt(a.ManufacturerData)
	if err == nil {
		payload := TiltPayload{
			Id:    b.Id,
			Color: TiltMap[b.Id],
			Major: b.Major,
			Minor: b.Minor,
			Rssi:  rssi,
		}

		level.Info(Logger).Log("main", fmt.Sprintf("%s [%s] temp: %d gravity: %d rssi: %d", payload.Id, payload.Color, payload.Major, payload.Minor, rssi))
	}
}

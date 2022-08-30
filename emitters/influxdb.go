package emitters

import (
	"bytes"
	"context"
	"crypto/tls"
	"encoding/json"
	"github.com/go-kit/log/level"
	influxdb2 "github.com/influxdata/influxdb-client-go/v2"
	"github.com/myoung34/tilty/tilt"
	"strconv"
	"text/template"
)

type InfluxDB struct {
	Enabled                    bool
	URL                        string `json:"url"`
	VerifySSL                  bool   `json:"verify_ssl"`
	Bucket                     string `json:"bucket"`
	Org                        string `json:"org"`
	Token                      string `json:"token"`
	GravityPayloadTemplate     string `json:"gravity_payload_template"`
	TemperaturePayloadTemplate string `json:"temperature_payload_template"`
}

//gravity_payload_template = gravity,color={{ color }},mac={{ mac }} sg={{ gravity }}
//temperature_payload_template = temperature,color={{ color }},mac={{ mac }} temp={{ temp }}

func InfluxDBEmit(payload tilt.Payload, emitterConfig interface{}) (string, error) {
	influxdb := InfluxDB{}
	jsonString, _ := json.Marshal(emitterConfig)
	json.Unmarshal(jsonString, &influxdb)

	client := influxdb2.NewClientWithOptions(influxdb.URL, influxdb.Token,
		influxdb2.DefaultOptions().
			SetTLSConfig(&tls.Config{
				InsecureSkipVerify: influxdb.VerifySSL,
			}))
	writeAPI := client.WriteAPIBlocking(influxdb.Org, influxdb.Bucket)

	payloadTemplate := Template{
		Color:     payload.Color,
		Gravity:   strconv.Itoa(int(payload.Minor)),
		Mac:       payload.Mac,
		Temp:      strconv.Itoa(int(payload.Major)),
		Timestamp: payload.Timestamp,
	}

	// Generate the gravity body from a template
	gravityTmpl, err := template.New("influxdb").Parse(`"gravity,color={{.Color}},mac={{.Mac}} sg={{.Gravity}}"`)
	if len(influxdb.GravityPayloadTemplate) > 0 {
		gravityTmpl, err = template.New("influxdb").Parse(influxdb.GravityPayloadTemplate)
	}
	if err != nil {
		level.Error(tilt.Logger).Log("emitters.influxdb", err)
		return "", err
	}
	var gravityTpl bytes.Buffer
	if err := gravityTmpl.Execute(&gravityTpl, payloadTemplate); err != nil {
		level.Error(tilt.Logger).Log("emitters.influxdb", err)
		return "", err
	}
	writeAPI.WriteRecord(context.Background(), gravityTpl.String())

	// Generate the temperature body from a template
	temperatureTmpl, err := template.New("influxdb").Parse(`"gravity,color={{.Color}},mac={{.Mac}} sg={{.Gravity}}"`)
	if len(influxdb.TemperaturePayloadTemplate) > 0 {
		temperatureTmpl, err = template.New("influxdb").Parse(influxdb.TemperaturePayloadTemplate)
	}
	if err != nil {
		level.Error(tilt.Logger).Log("emitters.influxdb", err)
		return "", err
	}
	var temperatureTpl bytes.Buffer
	if err := temperatureTmpl.Execute(&temperatureTpl, payloadTemplate); err != nil {
		level.Error(tilt.Logger).Log("emitters.influxdb", err)
		return "", err
	}
	writeAPI.WriteRecord(context.Background(), temperatureTpl.String())

	return "", nil
}

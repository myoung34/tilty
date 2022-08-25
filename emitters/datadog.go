package emitters

import (
	"encoding/json"
	"fmt"
	"github.com/DataDog/datadog-go/v5/statsd"
  "github.com/go-kit/log/level"
	"github.com/myoung34/tilty/tilt"
)

type Datadog struct {
	Enabled    bool
	StatsdHost string `json:"statsd_host"`
	StatsdPort int    `json:"statsd_port"`
}

func DatadogEmitWithClient(payload tilt.Payload, emitterConfig interface{}, client statsd.ClientInterface) (string, error) {

	defer client.Close()

	tags := []string{
		fmt.Sprintf("color:%s", payload.Color),
		fmt.Sprintf("mac:%s", payload.Mac),
	}
	level.Debug(tilt.Logger).Log("emitters.datadog", fmt.Sprintf("Temperature: %f, Tags: %v", float64(payload.Major), tags))
	client.Gauge("tilty.temperature",
		float64(payload.Major),
		tags,
		1,
	)
	level.Debug(tilt.Logger).Log("emitters.datadog", fmt.Sprintf("Gravity: %f, Tags: %v", float64(payload.Minor), tags))
	client.Gauge("tilty.gravity",
		float64(payload.Minor),
		tags,
		1,
	)

	return "", nil
}

func DatadogEmit(payload tilt.Payload, emitterConfig interface{}) (string, error) {
	datadog := Datadog{}
	jsonString, _ := json.Marshal(emitterConfig)
	json.Unmarshal(jsonString, &datadog)
	client, err := statsd.New(fmt.Sprintf("%s:%d", datadog.StatsdHost, datadog.StatsdPort))
	if err != nil {
		level.Error(tilt.Logger).Log("emitters.datadog", err)
		return "", err
	}
	return DatadogEmitWithClient(payload, emitterConfig, client)
}

package emitters

import (
	"github.com/DataDog/datadog-go/v5/statsd"
	"github.com/myoung34/tilty/tilt"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestDatadogEmit(t *testing.T) {
	tilt.EnableLogging()

	sampleConfig := tilt.ParseConfig("some/file/somewhere.toml")
	sampleConfig.ConfigData.Set("datadog.enabled", true)
	sampleConfig.ConfigData.Set("datadog.statsd_host", "testing")
	sampleConfig.ConfigData.Set("datadog.statsd_port", "8125")

	payload := tilt.TiltPayload{
		Id:        "0987654321",
		Mac:       "66:77:88:99:00",
		Color:     "BLACK",
		Major:     65,
		Minor:     1098,
		Rssi:      -7,
		Timestamp: 1661445284,
	}
	resp, err := DatadogEmitWithClient(payload, sampleConfig.ConfigData.Get("datadog"), &statsd.NoOpClient{})
	assert.Equal(t, nil, err)
	assert.Equal(t, "", resp)

	resp, err = DatadogEmit(payload, sampleConfig.ConfigData.Get("datadog"))
	assert.NotNil(t, err, "This should have failed DNS lookup")
	assert.Equal(t, "", resp)
}

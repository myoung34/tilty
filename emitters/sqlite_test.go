package emitters

import (
	"github.com/myoung34/tilty/tilt"
	"github.com/stretchr/testify/assert"
	"testing"
)

type AnyTime struct{}

func TestSQLite(t *testing.T) {
	tilt.EnableLogging()

	sampleConfig := tilt.ParseConfig("some/file/somewhere.toml")
	sampleConfig.ConfigData.Set("sqlite.enabled", true)
	sampleConfig.ConfigData.Set("sqlite.file", "foo.db")

	payload := tilt.Payload{
		ID:        "0987654321",
		Mac:       "66:77:88:99:00",
		Color:     "BLACK",
		Major:     65,
		Minor:     1098,
		Rssi:      -7,
		Timestamp: 1661445284,
	}
	resp, err := SQLiteEmit(payload, sampleConfig.ConfigData.Get("sqlite"))
	assert.Equal(t, nil, err)
	assert.Equal(t, "insert into data (gravity,temp,color,mac) values (1098,65,'BLACK','66:77:88:99:00')", resp)
}

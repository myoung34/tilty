package emitters

import (
	"bytes"
	"github.com/jarcoal/httpmock"
	"github.com/myoung34/tilty/tilt"
	"github.com/stretchr/testify/assert"
	"net/http"
	"testing"
)

type TiltWebhookTest struct {
	Type     string
	Payload  tilt.TiltPayload
	Enabled  bool
	Url      string
	Headers  string
	Template string
	Method   string
}

type TiltTest struct {
	Response      string
	CallCount     int
	CallSignature string
}

type convTest struct {
	name string
	in   TiltWebhookTest
	out  TiltTest
}

func TestWebhook(t *testing.T) {

	httpmock.Activate()
	defer httpmock.DeactivateAndReset()

	tilt.EnableLogging()

	theTests := []convTest{
		{
			name: "POST",
			in: TiltWebhookTest{
				Type: "webhook",
				Payload: tilt.TiltPayload{
					Id:        "1234567890",
					Mac:       "11:22:33:44:55",
					Color:     "RED",
					Major:     90,
					Minor:     1024,
					Rssi:      -67,
					Timestamp: "2009-11-10 23:00:00 +0000 UTC",
				},
				Enabled:  true,
				Url:      "http://something.com",
				Headers:  "{\"Content-Type\": \"application/json\", \"Foo\": \"bar\"}",
				Template: "{\"color\": \"{{ color }}\", \"gravity\": {{ gravity }}, \"mac\": \"{{ mac }}\", \"temp\": {{ temp }}, \"timestamp\": \"{{ timestamp }}\"}",
				Method:   "POST",
			},
			out: TiltTest{
				Response:      "{\"Response\":\"{\\\"name\\\": \\\"Tilt RED\\\", \\\"gravity\\\": 1024, \\\"gravity_unit\\\": \\\"G\\\", \\\"temp\\\": 90, \\\"temp_unit\\\": \\\"F\\\"}\"}",
				CallCount:     1,
				CallSignature: "POST http://something.com",
			},
		},
		{
			name: "GET",
			in: TiltWebhookTest{
				Type: "webhook",
				Payload: tilt.TiltPayload{
					Id:        "0987654321",
					Mac:       "66:77:88:99:00",
					Color:     "BLACK",
					Major:     65,
					Minor:     1098,
					Rssi:      -7,
					Timestamp: "2019-11-10 23:59:00 +0000 UTC",
				},
				Enabled:  true,
				Url:      "http://fake.com",
				Headers:  "{\"Content-Type\": \"application/json\"}",
				Template: "{\"color\": \"{{ color }}\", \"gravity\": {{ gravity }}, \"mac\": \"{{ mac }}\", \"temp\": {{ temp }}, \"timestamp\": \"{{ timestamp }}\"}",
				Method:   "GET",
			},
			out: TiltTest{
				Response:      "{\"Response\":\"{\\\"name\\\": \\\"Tilt BLACK\\\", \\\"gravity\\\": 1098, \\\"gravity_unit\\\": \\\"G\\\", \\\"temp\\\": 65, \\\"temp_unit\\\": \\\"F\\\"}\"}",
				CallCount:     2,
				CallSignature: "GET http://fake.com",
			},
		},
	}
	for _, theT := range theTests {

		httpmock.RegisterResponder(theT.in.Method, theT.in.Url,
			func(req *http.Request) (*http.Response, error) {
				buf := new(bytes.Buffer)
				buf.ReadFrom(req.Body)
				return httpmock.NewJsonResponse(200, map[string]interface{}{
					"Response": buf.String(),
				})
			},
		)
		t.Run(theT.name, func(t *testing.T) {
			sampleConfig := tilt.ParseConfig("some/file/somewhere.toml")

			sampleConfig.ConfigData.Set("webhook.url", theT.in.Url)
			sampleConfig.ConfigData.Set("webhook.headers", theT.in.Headers)
			sampleConfig.ConfigData.Set("webhook.template", theT.in.Template)
			sampleConfig.ConfigData.Set("webhook.method", theT.in.Method)
			resp, err := WebhookEmit(theT.in.Payload, sampleConfig.ConfigData.Get(theT.in.Type))
			assert.Equal(t, nil, err)
			assert.Equal(t, resp, theT.out.Response)
			assert.Equal(t, theT.out.CallCount, httpmock.GetTotalCallCount())
			info := httpmock.GetCallCountInfo()
			assert.Equal(t, 1, info[theT.out.CallSignature])
		})
	}
}

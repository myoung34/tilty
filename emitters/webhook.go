package emitters

import (
	"bytes"
	"encoding/json"
	"fmt"
  "github.com/go-kit/log/level"
	"github.com/myoung34/tilty/tilt"
	"io"
	"net/http"
	"strconv"
	"text/template"
)

type Webhook struct {
	Enabled  bool
	URL      string
	Headers  string
	Template string
	Method   string
}

func WebhookEmit(payload tilt.Payload, emitterConfig interface{}) (string, error) {
	webhook := Webhook{}
	jsonString, _ := json.Marshal(emitterConfig)
	json.Unmarshal(jsonString, &webhook)

	level.Info(tilt.Logger).Log("emitters.webhook", webhook.URL)
	level.Info(tilt.Logger).Log("emitters.webhook", fmt.Sprintf("%v", webhook.Enabled))
	level.Info(tilt.Logger).Log("emitters.webhook", fmt.Sprintf("%+v", webhook.Headers))
	level.Info(tilt.Logger).Log("emitters.webhook", fmt.Sprintf("%+v", webhook.Template))
	level.Info(tilt.Logger).Log("emitters.webhook", fmt.Sprintf("%+v", webhook.Method))

	client := &http.Client{}

	// Set up the body based on the template
	bodyTemplate := Template{
		Color:     payload.Color,
		Gravity:   strconv.Itoa(int(payload.Minor)),
		Mac:       payload.Mac,
		Temp:      strconv.Itoa(int(payload.Major)),
		Timestamp: payload.Timestamp,
	}
	level.Info(tilt.Logger).Log("emitters.webhook", fmt.Sprintf("%+v", payload))

	tmpl, err := template.New("webhook").Parse(`{"name": "Tilt {{.Color}}", "gravity": {{.Gravity}}, "gravity_unit": "G", "temp": {{.Temp}}, "temp_unit": "F"}`)
	if len(webhook.Template) > 0 {
		tmpl, err = template.New("webhook").Parse(webhook.Template)
	}
	if err != nil {
		level.Error(tilt.Logger).Log("emitters.webhook", err)
		return "", err
	}
	var tpl bytes.Buffer
	if err := tmpl.Execute(&tpl, bodyTemplate); err != nil {
		level.Error(tilt.Logger).Log("emitters.webhook", err)
		return "", err
	}
	bodyReader := bytes.NewReader(tpl.Bytes())

	// Set up the request
	req, err := http.NewRequest(webhook.Method, webhook.URL, bodyReader)
	if err != nil {
		level.Error(tilt.Logger).Log("emitters.webhook", err)
		return "", err
	}

	// Parse the headers and add them
	var result map[string]string
	json.Unmarshal([]byte(webhook.Headers), &result)
	for key, value := range result {
		req.Header.Add(key, value)
	}

	// Make the request
	resp, err := client.Do(req)
	if err != nil {
		level.Error(tilt.Logger).Log("emitters.webhook", err)
		return "", err
	}

	defer resp.Body.Close()

	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		level.Error(tilt.Logger).Log("emitters.webhook", err)
		return "", err
	}

	return string(respBody), nil
}

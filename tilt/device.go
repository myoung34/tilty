package tilt

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
	Id        string
	Mac       string
	Color     string `validate:"required"`
	Major     uint16
	Minor     uint16
	Rssi      int
	Timestamp int64
}

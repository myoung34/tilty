package tilt

import (
	"github.com/go-kit/kit/log"
	"github.com/go-kit/kit/log/level"
	"os"
)

var Logger log.Logger

func SetLogging() {
	Logger = log.NewLogfmtLogger(os.Stderr)
	Logger = level.NewFilter(Logger, level.AllowDebug())
	Logger = log.With(Logger, "ts", log.DefaultTimestampUTC)
}

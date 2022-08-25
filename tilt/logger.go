package tilt

import (
	"fmt"
	"github.com/go-kit/kit/log"
	"github.com/go-kit/kit/log/level"
	"os"
	"strings"
)

var Logger log.Logger

func EnableLogging() {
	Logger = log.NewLogfmtLogger(os.Stderr)
	Logger = level.NewFilter(Logger, level.AllowDebug())
	Logger = log.With(Logger, "ts", log.DefaultTimestampUTC)
}

func SetLogging(logLevel string) {
	Logger = log.NewLogfmtLogger(os.Stderr)

	switch strings.ToLower(logLevel) {
	case "all":
		Logger = level.NewFilter(Logger, level.AllowAll())
	case "debug":
		Logger = level.NewFilter(Logger, level.AllowDebug())
	case "info":
		Logger = level.NewFilter(Logger, level.AllowInfo())
	case "none":
		Logger = level.NewFilter(Logger, level.AllowNone())
	case "warn":
		Logger = level.NewFilter(Logger, level.AllowWarn())
	default:
		Logger = level.NewFilter(Logger, level.AllowInfo())
	}
	Logger = log.With(Logger, "ts", log.DefaultTimestampUTC)
	level.Info(Logger).Log("logger.SetLogging", fmt.Sprintf("Setting log level to %s", logLevel))
}

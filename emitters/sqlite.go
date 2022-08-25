package emitters

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"github.com/go-kit/kit/log/level"
	_ "github.com/mattn/go-sqlite3"
	"github.com/myoung34/tilty/tilt"
	"log"
)

type SQLite struct {
	Enabled bool
	File    string
}

func SQLiteEmit(payload tilt.TiltPayload, emitterConfig interface{}) (string, error) {
	sqlite := SQLite{}
	jsonString, _ := json.Marshal(emitterConfig)
	json.Unmarshal(jsonString, &sqlite)

	db, err := sql.Open("sqlite3", sqlite.File)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	sqlStmt := `
      CREATE TABLE IF NOT EXISTS data(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        gravity INTEGER,
        temp INTEGER,
        color VARCHAR(16),
        mac VARCHAR(17),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)
       `
	_, err = db.Exec(sqlStmt)
	if err != nil {
		level.Error(tilt.Logger).Log("emitters.sqlite", err)
		return "", err
	}

	insertStmt := fmt.Sprintf(
		"insert into data (gravity,temp,color,mac) values (%d,%d,'%s','%s')",
		int(payload.Minor),
		int(payload.Major),
		payload.Color,
		payload.Mac,
	)
	level.Debug(tilt.Logger).Log("emitters.sqlite", insertStmt)
	_, err = db.Exec(insertStmt)
	if err != nil {
		level.Error(tilt.Logger).Log("emitters.sqlite", err)
		return "", err
	}

	return insertStmt, nil
}
